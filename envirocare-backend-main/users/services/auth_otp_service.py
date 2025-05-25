from datetime import datetime
from dateutil.relativedelta import *
import random, string
from users.models import CustomUser
from django.core.cache import cache


class AuthOtpService:
    """
    This service is responsible for dispacthing an OTP and verifying it

    The dispatch method calls the notification service and dispatches an SMS/Email with
    the OTP. It returns a message if the OTP has been successfully sent.

    The verify_OTP method checks the validity of the OTP and returns a boolean.
    """

    def __init__(self, otp: str, user_id:str, pre_token:str) -> None:
        self.otp = otp
        self.user_id = user_id
        self.pre_token = pre_token

    def generate_code(self):
        """
        Generate an 8 character alpha numeric code
        """
        return ''.join(random.choices(string.digits, k=8))


    def dispatch_otp(self) -> str:
        """
        Send the OTP by calling the notification service

        #! The event of sending the notification should be done 
        #! in the background to avoid blocking of additional requests
        """

        # code = self.generate_code()
        # print(code)
        code = "000000"

        # Email the code

        try:
            print(code)
            user = CustomUser.objects.get(id = self.user_id)
            print(code)
        except Exception as e:
            print(e)
            return "failed"

        cache.set(self.user_id, {
            "otp":code,
            "time_stamp": datetime.now(),
            "pre_token": self.pre_token
        })

        return "success"


    def verify_OTP(self, pre_token: str) -> bool:

        cached_record = cache.get(self.user_id)

        if cached_record is not None:
            exactly_five_minutes_ago = datetime.now() - relativedelta(minutes=10)

            valid_pre_token = pre_token == cached_record.get('pre_token')
            print("pre_token: " + pre_token, "cache: " + cached_record.get("pre_token"))
            code_hasnt_expired = cached_record.get("time_stamp") > exactly_five_minutes_ago
            code_exists = cached_record.get("otp") == self.otp

            if code_hasnt_expired and code_exists and valid_pre_token:
                cache.delete(self.user_id)
                return True

        return False