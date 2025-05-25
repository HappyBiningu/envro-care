from django import forms
from django.core.exceptions import ValidationError
import re

def password_validator(value):
    valid_password = re.fullmatch(r'[A-Za-z0-9@#$%^&+=!()_\-]{8,}', value)
    if valid_password:
        print("Validated!!!!!")
    else:
        raise ValidationError(("Your password input must have at least one lowercase letter, one uppercase letter, special character, a number and must be at least 8 characters long."),
            params={"value": value},)

class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password', 'style':'width: 100%;padding: 12px 20px;margin: 8px 0;box-sizing: border-box;', 'type':'password'}), validators=[password_validator], required=True)
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm Password', 'style':'width: 100%;padding: 12px 20px;margin: 8px 0;box-sizing: border-box;', 'type':'password'}), validators=[password_validator], required=True)