import requests
import json
from django.conf import settings
from django.core.cache import cache
from .models import WhatsAppUser, MessageHistory, ResponseCache
from core.models.envirocare import Complaint, Comment, Organisation
from datetime import datetime, timedelta
import openai

class ChatGPTService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def analyze_complaint(self, description, location, affected_area):
        """Analyze complaint using ChatGPT to determine organization, impact, and severity"""
        prompt = f"""Analyze this environmental complaint and provide:
1. The most appropriate organization to handle it (EMA, ZINWA, or COUNCIL)
2. The environmental impact assessment
3. The severity level (HIGH, MEDIUM, or LOW)

Complaint Description: {description}
Location: {location}
Affected Area: {affected_area}

Provide the response in JSON format with these keys:
{{
    "organization": "organization_name",
    "impact": "detailed_impact_assessment",
    "severity": "severity_level"
}}"""

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an environmental expert who analyzes complaints and determines the appropriate organization to handle them, assesses environmental impact, and determines severity levels."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                required_fields = ['organization', 'impact', 'severity']
                if not all(field in result for field in required_fields):
                    print(f"Missing required fields in response: {result}")
                    return None
                return result
            except json.JSONDecodeError as e:
                print(f"Error parsing ChatGPT response as JSON: {str(e)}")
                print(f"Raw response: {response.choices[0].message.content}")
                return None
                
        except Exception as e:
            print(f"Error analyzing complaint with ChatGPT: {str(e)}")
            return None

class WhatsAppService:
    def __init__(self):
        self.api_url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        self.greetings = [
            "hi", "hello", "hey", "good morning", "good afternoon", 
            "good evening", "good night", "greetings", "greeting"
        ]
        self.exit_messages = [
            "bye", "goodbye", "see you", "see you later", "take care",
            "exit", "quit", "end", "stop"
        ]
        self.chatgpt_service = ChatGPTService()
        print(f"Initialized WhatsApp service with URL: {self.api_url}")  # Debug log
        
    def is_greeting(self, text):
        """Check if the message is a greeting"""
        text = text.lower().strip()
        return any(greeting in text for greeting in self.greetings)

    def is_exit_message(self, text):
        """Check if the message is an exit message"""
        text = text.lower().strip()
        return any(exit_msg in text for exit_msg in self.exit_messages)

    def send_welcome_message(self, phone_number, user):
        """Send welcome message to user"""
        if user.name:
            welcome_text = f"Welcome back, {user.name}! 👋\n\n"
        else:
            welcome_text = "Welcome to EnviroCare WhatsApp Bot! 👋\n\n"
            
        welcome_text += "Please select an option from the menu below:"
        
        sections = [
            {
                "title": "Main Menu",
                "rows": [
                    {
                        "id": "new_complaint",
                        "title": "New Complaint",
                        "description": "Report a new environmental issue"
                    },
                    {
                        "id": "check_status",
                        "title": "Check Status",
                        "description": "Check your complaint status"
                    },
                    {
                        "id": "add_comment",
                        "title": "Add Comment",
                        "description": "Add a comment to existing complaint"
                    },
                    {
                        "id": "my_complaints",
                        "title": "My Complaints",
                        "description": "View your complaint history"
                    }
                ]
            }
        ]
        
        return self.send_list_message(phone_number, "EnviroCare Menu", welcome_text, sections)

    def send_exit_message(self, phone_number, user):
        """Send exit message to user"""
        if user.name:
            exit_text = f"Goodbye, {user.name}! 👋\nThank you for using EnviroCare WhatsApp Bot.\nFeel free to message us again if you need any assistance."
        else:
            exit_text = "Goodbye! 👋\nThank you for using EnviroCare WhatsApp Bot.\nFeel free to message us again if you need any assistance."
        
        return self.send_text_message(phone_number, exit_text)

    def handle_greeting(self, user, phone_number):
        """Handle greeting messages"""
        print(f"Handling greeting for user: {phone_number}")  # Debug log
        user.current_state = "MAIN_MENU"
        user.save()
        return self.send_welcome_message(phone_number, user)

    def handle_exit(self, user, phone_number):
        """Handle exit messages"""
        print(f"Handling exit for user: {phone_number}")  # Debug log
        user.current_state = "INITIAL"
        user.save()
        return self.send_exit_message(phone_number, user)

    def send_text_message(self, phone_number, text):
        """Send a text message to a WhatsApp user"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {"body": text}
        }
        print(f"Sending text message to {phone_number}: {text}")  # Debug log
        response = self._make_request(payload)
        print(f"Text message response: {response}")  # Debug log
        return response

    def send_interactive_message(self, phone_number, header, body, buttons):
        """Send an interactive message with buttons"""
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {"type": "text", "text": header},
                "body": {"text": body},
                "action": {
                    "buttons": buttons
                }
            }
        }
        return self._make_request(payload)

    def send_list_message(self, phone_number, header, body, sections):
        """Send an interactive list message"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": header},
                "body": {"text": body},
                "action": {
                    "button": "Menu",  # Required button label
                    "sections": sections
                }
            }
        }
        print(f"Sending list message to {phone_number}")  # Debug log
        response = self._make_request(payload)
        print(f"List message response: {response}")  # Debug log
        return response

    def _make_request(self, payload):
        """Make the actual API request"""
        print(f"Making request with payload: {json.dumps(payload, indent=2)}")  # Debug log
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            print(f"API Response status: {response.status_code}")  # Debug log
            print(f"API Response headers: {response.headers}")  # Debug log
            print(f"API Response body: {response.text}")  # Debug log
            return response.json()
        except Exception as e:
            print(f"Error making API request: {str(e)}")  # Debug log
            raise

    def get_or_create_user(self, phone_number):
        """Get or create a WhatsApp user"""
        user, created = WhatsAppUser.objects.get_or_create(phone_number=phone_number)
        if created:
            print(f"Created new user: {phone_number}")  # Debug log
        else:
            print(f"Found existing user: {phone_number}")  # Debug log
        return user

    def save_message(self, user, message_id, content, is_from_user=True):
        """Save a message to history"""
        message = MessageHistory.objects.create(
            user=user,
            message_id=message_id,
            message_type='text',
            content=content,
            is_from_user=is_from_user
        )
        print(f"Saved message: {message_id}")  # Debug log
        return message

    def get_cached_response(self, key):
        """Get a cached response"""
        cache_key = f"whatsapp_response_{key}"
        response = cache.get(cache_key)
        print(f"Getting cached response for key: {key}")  # Debug log
        return response

    def cache_response(self, key, response, expire_minutes=60):
        """Cache a response"""
        cache_key = f"whatsapp_response_{key}"
        cache.set(cache_key, response, expire_minutes * 60)
        print(f"Cached response for key: {key}")  # Debug log

    def create_complaint(self, user, description, location, affected_area):
        """Create a new complaint with AI analysis"""
        # Analyzing the complaint using ChatGPT
        analysis = self.chatgpt_service.analyze_complaint(description, location, affected_area)
        
        if not analysis:
            return None, "Error analyzing complaint. Please try again."

        # Getting or creating the organization
        org_name = analysis['organization'].upper()
        try:
            organisation = Organisation.objects.get(name__iexact=org_name)
        except Organisation.DoesNotExist:
            return None, f"Organization {org_name} not found in the system."

        # Creating the complaint with AI analysis
        complaint = Complaint.objects.create(
            organisation=organisation,
            description=description,
            location=location,
            affected_area=affected_area,
            environmental_impact=analysis['impact'],
            severity=analysis['severity'],
            reported_by_name=user.name or "WhatsApp User",
            reported_by_number=user.phone_number
        )
        
        return complaint, None

    def create_comment(self, user, description, ref=None):
        """Creating a new comment"""
        comment = Comment.objects.create(
            ref=ref,
            description=description,
            commented_by_name=user.name or "WhatsApp User",
            commented_by_number=user.phone_number
        )
        print(f"Created comment: {comment.id}")  
        return comment

    def get_complaint_status(self, ref):
        """Getting the status of a complaint"""
        try:
            complaint = Complaint.objects.get(ref=ref)
            status = {
                'ref': complaint.ref,
                'status': 'Resolved' if complaint.is_resolved else 'Pending',
                'resolved_date': complaint.resolved_date.strftime('%Y-%m-%d %H:%M') if complaint.resolved_date else None,
                'description': complaint.description
            }
            print(f"Got complaint status for ref: {ref}")  
            return status
        except Complaint.DoesNotExist:
            print(f"Complaint not found for ref: {ref}")  
            return None 

    def create_task(self, user, description, location, affected_area):
        """Create a new task with AI analysis"""
        # Analyze task using ChatGPT
        analysis = self.chatgpt_service.analyze_task(description, location, affected_area)
        
        if not analysis:
            return None, "Error analyzing task. Please try again."

        # Get or create the organization
        org_name = analysis['organization'].upper()
        try:
            organisation = Organisation.objects.get(name__iexact=org_name)
        except Organisation.DoesNotExist:
            return None, f"Organization {org_name} not found in the system."

        # Check for similar complaints at the same location
        similar_complaints = Complaint.objects.filter(
            location__icontains=location,
            status__in=['PENDING', 'IN_PROGRESS']
        ).exclude(
            description__isnull=True
        ).order_by('-created_at')[:3]

        # Create the task
        task = Task.objects.create(
            organisation=organisation,
            description=description,
            location=location,
            affected_area=affected_area,
            environmental_impact=analysis['impact'],
            severity=analysis['severity'],
            assigned_to_name=user.name or "WhatsApp User",
            assigned_to_number=user.phone_number
        )
        
        # Prepare response message
        response_message = f"Task created successfully!\n\nReference: {task.ref}\nOrganization: {task.organisation.name}\nSeverity: {task.severity}\nEnvironmental Impact: {task.environmental_impact}"
        
        # Add similar complaints information if found
        if similar_complaints.exists():
            response_message += "\n\n⚠️ Similar complaints found at this location:"
            for complaint in similar_complaints:
                response_message += f"\n- Complaint Ref: {complaint.ref} (Status: {complaint.status})"
        
        return task, response_message 

    def send_complaint_filters(self, phone_number):
        """Send complaint filter options"""
        header = "Filter Complaints"
        body = "Please select how you want to view your complaints:"
        
        sections = [
            {
                "title": "Filter Options",
                "rows": [
                    {
                        "id": "filter_all",
                        "title": "All Complaints",
                        "description": "View all your complaints"
                    },
                    {
                        "id": "filter_pending",
                        "title": "Pending",
                        "description": "View pending complaints"
                    },
                    {
                        "id": "filter_in_progress",
                        "title": "In Progress",
                        "description": "View in-progress complaints"
                    },
                    {
                        "id": "filter_completed",
                        "title": "Completed",
                        "description": "View completed complaints"
                    }
                ]
            }
        ]
        
        return self.send_list_message(phone_number, header, body, sections)

    def get_user_complaints(self, phone_number, filter_status=None):
        """Get complaints for a specific user with optional status filter"""
        complaints = Complaint.objects.filter(reported_by_number=phone_number)
        
        if filter_status:
            if filter_status == 'completed':
                complaints = complaints.filter(is_resolved=True)
            elif filter_status == 'pending':
                complaints = complaints.filter(is_resolved=False)
            elif filter_status == 'in_progress':
                complaints = complaints.filter(is_resolved=False)
        
        return complaints.order_by('-created_at')

    def format_complaints_message(self, complaints):
        """Format complaints into a beautiful message"""
        if not complaints.exists():
            return "You haven't submitted any complaints yet."

        message = "📋 Your Complaints:\n\n"
        
        for complaint in complaints:
            # Get status emoji based on resolution
            status_emoji = '✅' if complaint.is_resolved else '⏳'
            
            # Format date
            date_str = complaint.created_at.strftime('%Y-%m-%d')
            
            # Create complaint summary
            message += f"{status_emoji} *Complaint #{complaint.ref}*\n"
            message += f"📅 Date: {date_str}\n"
            message += f"🏢 Organization: {complaint.organisation.name}\n"
            message += f"📍 Location: {complaint.location}\n"
            message += f"⚠️ Severity: {complaint.severity}\n"
            message += f"📝 Description: {complaint.description[:100]}...\n"
            message += f"🔄 Status: {'Resolved' if complaint.is_resolved else 'Pending'}\n"
            if complaint.is_resolved:
                message += f"✅ Resolved: {complaint.resolved_date.strftime('%Y-%m-%d')}\n"
            message += "\n"  # Add spacing between complaints
        
        return message 