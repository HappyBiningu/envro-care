# from rest_framework import serializers
# from django.utils.encoding import smart_bytes, smart_str, force_str
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# # from django.contrib.auth.models import User
# from users.models import CustomUser
# from rest_framework.exceptions import AuthenticationFailed


# class RequestPasswordResetEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)

#     class Meta:
#         fields = ['email']

# class SetNewPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(min_length=7, max_length=50, write_only=True)
#     token = serializers.CharField(min_length=1, write_only=True)
#     uid64 = serializers.CharField(min_length=1, write_only=True)

#     class Meta:
#         fields = ['password', 'token', 'uid64']

#     def validate(self, attrs):
        
#         try:
#             password = attrs.get('password')
#             token = attrs.get('token')
#             uid64 = attrs.get('uid64')

#             id = force_str(urlsafe_base64_decode(uid64))
#             user = CustomUser.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed('reset link is invalid', 401)

#             user.set_password(password)

#             user.save()
            
#             return (user)

#         except Exception as err:
#             print(err)
#             raise AuthenticationFailed('reset link is invalid', 401)