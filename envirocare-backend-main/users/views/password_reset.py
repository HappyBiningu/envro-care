# from rest_framework import generics
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError, force_str
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth import get_user_model
# from rest_framework.response import Response
# from safi.settings import APPLICATION_HOST
# from django.template.response import TemplateResponse
# from ..forms.password_reset_form import PasswordResetForm
# from users.models import CustomUser

# from ..tasks.send_email import send_password_reset

# User = get_user_model()

# class RequestPasswordResetEmail(generics.GenericAPIView):
    

#     def post(self, request):
#         email = request.data.get('email', '')

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uid64 = urlsafe_base64_encode(smart_bytes(user.id)) # encode user ID in bytes and convert to UID
#             token = PasswordResetTokenGenerator().make_token(user) # token with user details
            
#             abs_url = f"{APPLICATION_HOST}/api/v1/password-reset/{uid64}/{token}"
                                               
#             send_password_reset.delay(user.email, abs_url)

#             return Response({'success': 'We are sending you a link to reset your password'}, status=200)

#         else:
#             return Response({"error": "Email does not exist"}, status=400)

# class PasswordCheckTokenAPIView(generics.GenericAPIView):

#     def get(self, request, uid64, token):
#         try:
#             user_id = smart_str(urlsafe_base64_decode(uid64))
#             user = User.objects.get(id=user_id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error': 'Your Token is invalid, please request a new one'})
#             return Response({'success': 'True', 'message': 'Credentials are valid', 'uid64': uid64, 'token': token}, status=200)

#         except DjangoUnicodeDecodeError as identifier:
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error': 'Your Token is invalid, please request a new one'})

# class SetNewPassword(generics.GenericAPIView):
#     # serializer_class = SetNewPasswordSerializer

#     def patch(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         return Response({'success': True, 'message': 'Password reset success'}, status=200)
    
# def reset_password(request, uid64, token):
#     form = PasswordResetForm(request.POST or None)
#     context = {"form":form, "status":True, "message":"", "success":False}

#     try:
#         user_id = smart_str(urlsafe_base64_decode(uid64))
#         user = User.objects.get(id=user_id)

#         if not PasswordResetTokenGenerator().check_token(user=user, token=token):
#             context["message"] = "Invalid reset link. Please re-request the token again from your login screen."
#             context["status"] = False

#     except DjangoUnicodeDecodeError as identifier:
#         if not PasswordResetTokenGenerator().check_token(user=user, token=token):
#             context["message"] = "Invalid reset link. Please re-request the token again from your login screen."
#             context["status"] = False

#     if request.method == 'POST':
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         passwords_match = password == password2
        
#         if passwords_match and form.is_valid():
#             id = force_str(urlsafe_base64_decode(uid64))
#             user = CustomUser.objects.get(id=id)
#             if PasswordResetTokenGenerator().check_token(user, token) is not True:
#                 context["message"] = "Invalid reset link. Please re-request the token again from your login screen."
#                 context["status"] = False
#             else:
#                 user.set_password(password)
#                 user.save()
#                 context["success"] = True
#         else:
#             context["message"] = "Your passwords do not match." if passwords_match is not True else "Invalid password."
#             context["status"] = False

#     return TemplateResponse(request, "forgot_password.html", context)