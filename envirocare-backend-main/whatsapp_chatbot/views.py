from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
from .services import WhatsAppService
from .models import WhatsAppUser

# Create your views here.

@csrf_exempt
@require_http_methods(["GET", "POST"])
def webhook(request):
    """Handle both webhook verification and incoming messages"""
    if request.method == "GET":
        # Handle webhook verification
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
                return HttpResponse(challenge, status=200)
        return HttpResponse(status=403)
    
    elif request.method == "POST":
        # Handle incoming messages
        whatsapp_service = WhatsAppService()
        
        try:
            data = json.loads(request.body)
            print(f"Received webhook data: {json.dumps(data, indent=2)}")  # Debug log
            
            # Process the message
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            
            # Get user info from contacts
            contacts = value.get("contacts", [])
            if contacts:
                contact = contacts[0]
                user_name = contact.get("profile", {}).get("name")
                phone_number = contact.get("wa_id")
            else:
                phone_number = None
                user_name = None
            
            # Get message details
            messages = value.get("messages", [])
            if not messages:
                return HttpResponse(status=200)
                
            message = messages[0]
            message_id = message["id"]
            message_type = message["type"]
            
            print(f"Processing message from {phone_number}")  # Debug log
            
            if not phone_number:
                print("No phone number found in message")  # Debug log
                return HttpResponse(status=200)
            
            # Get or create user
            user = whatsapp_service.get_or_create_user(phone_number)
            if user_name and not user.name:
                user.name = user_name
                user.save()
            
            # Handle different message types
            if message_type == "text":
                text = message["text"]["body"]
                print(f"Received text message: {text}")  # Debug log
                whatsapp_service.save_message(user, message_id, text)
                
                # Process the message based on user's current state
                response = process_message(user, text, whatsapp_service)
                if response:
                    print(f"Sending response: {response}")  # Debug log
                    if isinstance(response, dict):
                        # Send the main message first
                        whatsapp_service.send_text_message(phone_number, response['message'])
                        # Then send the menu if needed
                        if response.get('message'):
                            whatsapp_service.send_text_message(phone_number, response['message'])
                        # Then send the menu if needed
                        if response.get('show_menu'):
                            whatsapp_service.send_welcome_message(phone_number, user)
                    else:
                        whatsapp_service.send_text_message(phone_number, response)
                else:
                    print("No response to send")  # Debug log
                
            elif message_type == "interactive":
                interactive = message["interactive"]
                if interactive["type"] == "button_reply":
                    button_id = interactive["button_reply"]["id"]
                    response = process_button_click(user, button_id, whatsapp_service)
                    if response:
                        whatsapp_service.send_text_message(phone_number, response)
                elif interactive["type"] == "list_reply":
                    list_id = interactive["list_reply"]["id"]
                    response = process_list_selection(user, list_id, whatsapp_service)
                    if response:
                        whatsapp_service.send_text_message(phone_number, response)
            
            return HttpResponse(status=200)
            
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return HttpResponse(status=500)

def process_message(user, text, whatsapp_service):
    """Process incoming text messages"""
    print(f"Processing message for user {user.phone_number}: {text}")  # Debug log
    if whatsapp_service.is_greeting(text):
        return whatsapp_service.handle_greeting(user, user.phone_number)
    
    # Check for greetings
    if whatsapp_service.is_greeting(text):
        return whatsapp_service.handle_greeting(user, user.phone_number)
        
    # Check for exit messages
    if whatsapp_service.is_exit_message(text):
        return whatsapp_service.handle_exit(user, user.phone_number)
    
    state = user.current_state
    
    # Handle follow-up responses
    if state.startswith("FOLLOW_UP_"):
        if text == "1":
            user.current_state = "MAIN_MENU"
            user.state_data = {}
            user.save()
            return whatsapp_service.send_welcome_message(user.phone_number, user)
        elif text == "2":
            return whatsapp_service.handle_exit(user, user.phone_number)
        else:
            return "Please select a valid option (1 or 2)."
            
    elif state == "FOLLOW_UP_FILTER":
        if text == "1":
            user.current_state = "COMPLAINT_FILTERS"
            user.state_data = {}
            user.save()
            return whatsapp_service.send_complaint_filters(user.phone_number)
        elif text == "2":
            user.current_state = "MAIN_MENU"
            user.state_data = {}
            user.save()
            return whatsapp_service.send_welcome_message(user.phone_number, user)
        else:
            return "Please select a valid option (1 or 2)."

    # Handle different message types
    if state == "INITIAL":
        print("User in INITIAL state, sending welcome message")  # Debug log
        user.current_state = "MAIN_MENU"
        user.save()
        whatsapp_service.send_welcome_message(user.phone_number, user)
        return None
        
    elif state == "MAIN_MENU":
        print(f"User in MAIN_MENU state, processing text: {text}")  # Debug log
        if text.lower() in ["1", "complaint", "new complaint"]:
            user.current_state = "COMPLAINT_DESCRIPTION"
            user.save()
            return "Please describe your complaint in detail:"
            
        elif text.lower() in ["2", "status", "check status"]:
            user.current_state = "CHECK_STATUS"
            user.save()
            return "Please enter your complaint reference number (e.g., REP123):"
            
        elif text.lower() in ["3", "comment", "add comment"]:
            user.current_state = "COMMENT_REF"
            user.save()
            return "Please enter the complaint reference number you want to comment on (or type 'new' for a new comment):"
            
        else:
            print("Invalid menu option, sending welcome message")  # Debug log
            whatsapp_service.send_welcome_message(user.phone_number, user)
            return None
            
    elif state == "COMPLAINT_DESCRIPTION":
        # Initialize state_data if it doesn't exist
        if not user.state_data:
            user.state_data = {}
        
        # Store the description
        user.state_data['description'] = text
        user.current_state = "COMPLAINT_LOCATION"
        user.save()
        return "Please provide the location of the incident:"
        
    elif state == "COMPLAINT_LOCATION":
        # Store the location
        user.state_data['location'] = text
        user.current_state = "COMPLAINT_AREA"
        user.save()
        return "How big is the affected area (Big / Medium / Small):"
        
    elif state == "COMPLAINT_AREA":
        # Store the affected area
        user.state_data['affected_area'] = text
        
        # Create the complaint with AI analysis
        complaint, error = whatsapp_service.create_complaint(
            user=user,
            description=user.state_data.get('description', ''),
            location=user.state_data.get('location', ''),
            affected_area=user.state_data.get('affected_area', '')
        )
        
        if error:
            response = {
                "message": f"Error creating complaint: {error}",
                "show_menu": True
            }
            user.current_state = "MAIN_MENU"
            user.state_data = {}
            user.save()
            return response
            
        # Clear state data and update user state
        user.current_state = "FOLLOW_UP_COMPLAINT"
        user.state_data = {}
        user.save()
        
        response = {
            "message": f"Complaint submitted successfully!\n\nReference: {complaint.ref}\nOrganization: {complaint.organisation.name}\nSeverity: {complaint.severity}\nEnvironmental Impact: {complaint.environmental_impact}\n\nWould you like to:\n1. Continue with another action\n2. End conversation",
            "show_menu": False
        }
        return response
        
    elif state == "COMPLAINT_IMPACT":
        # Getting all stored data
        description = whatsapp_service.get_cached_response(f"complaint_desc_{user.phone_number}")
        location = whatsapp_service.get_cached_response(f"complaint_loc_{user.phone_number}")
        affected_area = whatsapp_service.get_cached_response(f"complaint_area_{user.phone_number}")
        
        # Creating the complaint
        complaint, error = whatsapp_service.create_complaint(
            user, description, location, affected_area, text
        )
        
        # Resetting user state to follow-up
        user.current_state = "FOLLOW_UP_COMPLAINT"
        user.save()
        
        if complaint:
            return {
                'message': f"Your complaint has been registered successfully!\nReference number: {complaint.ref}\n\nWould you like to:\n1. Continue with another action\n2. End conversation",
                'show_menu': False
            }
        else:
            return {
                'message': f"Error: {error}\n\nWould you like to:\n1. Try again\n2. End conversation",
                'show_menu': False
            }
            
    elif state == "CHECK_STATUS":
        status = whatsapp_service.get_complaint_status(text)
        # Resetting user state to follow-up
        user.current_state = "FOLLOW_UP_STATUS"
        user.save()
        
        if status:
            return {
                'message': f"Complaint Status:\nReference: {status['ref']}\nStatus: {status['status']}\nResolved Date: {status['resolved_date'] or 'Not resolved'}\nDescription: {status['description']}\n\nWould you like to:\n1. Check another complaint\n2. End conversation",
                'show_menu': False
            }
        else:
            return {
                'message': f"Complaint not found. Please check the reference number and try again.\n\nWould you like to:\n1. Check another complaint\n2. End conversation",
                'show_menu': False
            }
            
    elif state == "COMMENT_REF":
        if text.lower() == "new":
            user.current_state = "COMMENT_DESCRIPTION"
            user.save()
            return "Please enter your comment:"
        else:
            user.current_state = "COMMENT_DESCRIPTION"
            user.save()
            whatsapp_service.cache_response(f"comment_ref_{user.phone_number}", text)
            return "Please enter your comment:"
            
    elif state == "COMMENT_DESCRIPTION":
        ref = whatsapp_service.get_cached_response(f"comment_ref_{user.phone_number}")
        comment = whatsapp_service.create_comment(user, text, ref)
        
        # Resetting user state to follow-up
        user.current_state = "FOLLOW_UP_COMMENT"
        user.save()
        
        return {
            'message': f"Your comment has been added successfully!\n\nWould you like to:\n1. Add another comment\n2. End conversation",
            'show_menu': False
        }

    elif state == "TASK_AREA":
        # Storing the affected area
        user.state_data['affected_area'] = text
        
        # Creating the task with AI analysis
        task, response_message = whatsapp_service.create_task(
            user=user,
            description=user.state_data.get('description', ''),
            location=user.state_data.get('location', ''),
            affected_area=user.state_data.get('affected_area', '')
        )
        
        if not task:
            response = {
                "message": response_message,
                "show_menu": True
            }
            user.current_state = "MAIN_MENU"
            user.state_data = {}
            user.save()
            return response
            
        # Clear state data and update user state
        user.current_state = "FOLLOW_UP_TASK"
        user.state_data = {}
        user.save()
        
        response = {
            "message": f"{response_message}\n\nWould you like to:\n1. Continue with another action\n2. End conversation",
            "show_menu": False
        }
        return response

def process_button_click(user, button_id, whatsapp_service):
    """Process button click interactions"""
    print(f"Processing button click: {button_id}")  # Debug log
    
    if button_id == "new_complaint":
        user.current_state = "COMPLAINT_DESCRIPTION"
        user.state_data = {}
        user.save()
        return whatsapp_service.send_text_message(user.phone_number, "How big is the affected area (Big / Medium / Small):")
        
    elif button_id == "check_status":
        user.current_state = "CHECK_STATUS"
        user.save()
        return whatsapp_service.send_text_message(user.phone_number, "Please enter your complaint reference number:")
        
    elif button_id == "add_comment":
        user.current_state = "COMMENT_REF"
        user.save()
        return whatsapp_service.send_text_message(user.phone_number, "Please enter the complaint reference number:")
        
    elif button_id == "my_complaints":
        user.current_state = "COMPLAINT_FILTERS"
        user.save()
        return whatsapp_service.send_complaint_filters(user.phone_number)
        
    elif button_id.startswith("filter_"):
        filter_type = button_id.replace("filter_", "")
        complaints = whatsapp_service.get_user_complaints(user.phone_number, filter_type)
        message = whatsapp_service.format_complaints_message(complaints)
        
        # Add follow-up options
        message += "\n\nWould you like to:\n1. View different filter\n2. Return to main menu"
        
        user.current_state = "FOLLOW_UP_FILTER"
        user.state_data = {"filter_type": filter_type}
        user.save()
        
        return whatsapp_service.send_text_message(user.phone_number, message)
        
    return whatsapp_service.send_text_message(user.phone_number, "Invalid option selected. Please try again.")

def process_list_selection(user, list_id, whatsapp_service):
    """Process list selection interactions"""
    return process_button_click(user, list_id, whatsapp_service)

def show_main_menu():
    """Show the main menu options"""
    return """Welcome to EnviroCare WhatsApp Bot! Please select an option:

1. New Complaint
2. Check Complaint Status
3. Add Comment

Type the number or option name to proceed."""
