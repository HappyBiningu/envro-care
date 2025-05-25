from django.db import models
import uuid

class WhatsAppUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    current_state = models.CharField(max_length=50, default="INITIAL")
    state_data = models.JSONField(null=True, blank=True)  # Store temporary state data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.phone_number})"

    class Meta:
        verbose_name = 'WhatsApp User'
        verbose_name_plural = 'WhatsApp Users'
        ordering = ['-created_at']

class MessageHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(WhatsAppUser, on_delete=models.CASCADE, related_name='messages')
    message_id = models.CharField(max_length=255)
    message_type = models.CharField(max_length=50)
    content = models.TextField()
    is_from_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.message_type}"

    class Meta:
        verbose_name = 'Message History'
        verbose_name_plural = 'Message Histories'
        ordering = ['-created_at']

class ResponseCache(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.key} - {self.created_at}"

    class Meta:
        verbose_name = 'Response Cache'
        verbose_name_plural = 'Response Caches'
        ordering = ['-created_at']
