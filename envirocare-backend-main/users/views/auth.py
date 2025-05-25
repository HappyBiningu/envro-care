import uuid
from django.core import exceptions
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView

from users.serializers.user import CustomUserSerializer
from users.services.auth_otp_service import AuthOtpService
from ..models import CustomUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    token = {"refresh": str(refresh), "access": str(refresh.access_token)}
    return token


def get_user(email):
    try:
        return CustomUser.objects.get(email=email.lower())
    except exceptions.ObjectDoesNotExist:
        return None

class HttpOnlyLoginView(APIView):
    def post(self, request, format=None):
        response = Response()
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
        try:
            user = get_user(email)
            if user is not None:
                is_staff = user.is_staff
                is_active = user.is_active
                
                if is_active and is_staff:
                    authenticate_user = authenticate(username=user.username, password=password)
                    if authenticate_user is not None:

                        token = get_tokens_for_user(user)

                        response.set_cookie(
                            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                            value=token["access"],
                            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                        )
                        
                        csrf.get_token(request)

                        response.data = {"success": "Verification successful"}

                        return response
                    else:
                        return Response({"error": "Invalid email or password!!"},status=status.HTTP_401_UNAUTHORIZED,)
                else:
                    return Response({"error": "This account is not active!!"}, status=status.HTTP_401_UNAUTHORIZED,)
            else:
                return Response({"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND,)
                
        except Exception as error:
            print(error)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DesktopLogin(APIView):
    def post(self, request, format=None):
        response = Response()
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        data = {"Success": "Verification successful"}
        
        try:
            user = get_user(email)
            if user is not None:
                is_active = user.is_active
                
                if is_active:
                    authenticate_user = authenticate(username=user.username, password=password)
                    if authenticate_user is not None:
                        # data["user"] = CustomUserSerializer(user).data
                        data["email"] = user.email
                        data["full_name"] = user.full_name
                        token = get_tokens_for_user(user)
                        data["token"] = token["access"]
                        response.data = data

                        return response
                    else:
                        return Response({"error": "Invalid email or password!!"},status=status.HTTP_401_UNAUTHORIZED,)
                else:
                    return Response({"error": "This account is not active!!"}, status=status.HTTP_401_UNAUTHORIZED,)
            else:
                return Response({"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND,)
                
        except Exception as error:
            print(error)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MobileLogin(APIView):
    def post(self, request, format=None):
        response = Response()
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        data = {"Success": "Verification successful"}
        
        try:
            user = get_user(email)
            if user is not None:
                is_active = user.is_active
                is_staff = user.is_superuser
                
                if is_active and is_staff:
                    authenticate_user = authenticate(username=user.username, password=password)
                    if authenticate_user is not None:
                        # data["user"] = CustomUserSerializer(user).data
                        data["email"] = user.email
                        data["full_name"] = user.full_name
                        token = get_tokens_for_user(user)
                        data["token"] = token["access"]
                        response.data = data

                        return response
                    else:
                        return Response({"error": "Invalid email or password!!"},status=status.HTTP_401_UNAUTHORIZED,)
                else:
                    return Response({"error": "This account is not active!!"}, status=status.HTTP_401_UNAUTHORIZED,)
            else:
                return Response({"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND,)
                
        except Exception as error:
            print(error)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# class ResendOTP(APIView):

#     def get(self, request):
#         user_id = request.query_params.get("user_id")
#         pre_token = request.query_params.get("pre_token")
#         user_obj = CustomUser.objects.filter(id = user_id)
#         if user_obj.exists():
#             AuthOtpService(otp=None ,user_id=user_id, pre_token=pre_token).dispatch_otp()
#             return Response({"success": True}, status=status.HTTP_200_OK)
        
#         return Response({"error": "This user does not exist."}, status=status.HTTP_404_NOT_FOUND)
# class VerifyAuthOtp(APIView):

#     def post(self, request):
#         """
#             The view is responsible for verifying the validity of the OTP
#             then assigning HTTP only authentication cookies.
#         """
#         response = Response()
#         otp = request.data.get("otp")
#         user_id = request.data.get("user_id")
#         pre_token = request.data.get("pre_token")
#         user = CustomUser.objects.get(id=user_id)

#         verification_status = AuthOtpService(otp, user_id, pre_token="").verify_OTP(pre_token)

#         if verification_status is True:
#             token = get_tokens_for_user(user)

#             response.set_cookie(
#                 key=settings.SIMPLE_JWT["AUTH_COOKIE"],
#                 value=token["access"],
#                 expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
#                 secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
#                 httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
#                 samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
#             )
            
#             csrf.get_token(request)

#             response.data = {"Success": "Verification successful"}

#             return response


#         return Response({"failed": "Failed to verify code. Try again"}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """Post request to log out user by deleting and set the token expiration time to 0sec"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        response = Response()
        token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        # cache_key = "chat-cached-user" + str(request.user.id)

        try:
            del_token = response.delete_cookie(token, path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"])
            if del_token is None:
                response.set_cookie(key=settings.SIMPLE_JWT["AUTH_COOKIE"], value=token, max_age=0)
                response.data = {"success": "Logout successfully."}
                # cache.delete(cache_key)
                return response
            else:
                pass
        except Exception as err:
            print(err)
            return Response(data={"error": "Failed to log out."}, status=400)
        

class VerifyMobileAuthOTP(APIView):
    def post(self, request, *args, **kwargs):
        response = Response()
        otp = request.data.get("otp")
        user_id = request.data.get("user_id")
        pre_token = request.data.get("pre_token")
        user = CustomUser.objects.get(id=user_id)
        data = {"Success": "Verification successful"}

        verification_status = AuthOtpService(otp, user_id, pre_token="").verify_OTP(pre_token)

        if verification_status is True:
            token = get_tokens_for_user(user)
            data["token"] = token["access"]
            data["user"] = CustomUserSerializer(user).data
            response.data = data

            return response


        return Response({"error": "Failed to verify code.", "messgae":"Invalid pre_token or otp code"}, status=status.HTTP_400_BAD_REQUEST)

class XtenMobileLoginView(APIView):

    def post(self, request, format=None):
        response = Response()
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
        try:
            user = get_user(email)
            if user is not None:
                is_active = user.is_active
                is_staff = user.is_superuser
                
                if is_active and is_staff:
                    authenticate_user = authenticate(username=user.username, password=password)
                    if authenticate_user is not None:

                        user_id = authenticate_user.id
                        pre_token = str(uuid.uuid4())

                        AuthOtpService(otp=None ,user_id=user_id, pre_token=pre_token).dispatch_otp()
                        
                        response.data = {"Success": "Login successful", "user_id": user_id, "pre_token": pre_token}

                        return response
                    else:
                        return Response({"error": "Invalid email or password!!"},status=status.HTTP_401_UNAUTHORIZED,)
                else:
                    return Response({"error": "This account is not active!!"}, status=status.HTTP_401_UNAUTHORIZED,)
            else:
                return Response({"error": "User does not exists."}, status=status.HTTP_404_NOT_FOUND,)
                
        except Exception as error:
            print(error)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
