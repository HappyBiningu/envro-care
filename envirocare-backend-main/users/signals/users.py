from django.db.models.signals import pre_save
from django.dispatch import receiver
from ..models import CustomUser



@receiver(pre_save, sender=CustomUser, dispatch_uid="save_username_as_email")
def save_username_as_email(sender, instance, *args, **kwargs):
    instance.username = instance.email