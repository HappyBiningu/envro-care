from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

SEX = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHER", "OTHER"),
    ("UNSPECIFIED", "UNSPECIFIED")
)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=25, choices=SEX)
    id_number = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=13, null=True)
    date_of_birth = models.DateField(null=True)
    profile_photo = models.ImageField(null=True)

    # Permission levels

    low_permissions = models.BooleanField(default=False)
    medium_permissions = models.BooleanField(default=False)
    high_permissions = models.BooleanField(default=False)
    super_permissions = models.BooleanField(default=False)
    ultra_permissions = models.BooleanField(default=False)
    extreme_permissions = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_joined"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_user_by_email(cls, email):
        return cls.objects.get(email=email)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects.get(username=username)

    @classmethod
    def get_user_by_id(cls, ID):
        return cls.objects.get(ID=ID)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"