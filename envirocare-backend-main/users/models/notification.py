# from django.db import models
# import uuid


# class Notification(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey("users.CustomUser", on_delete=models.RESTRICT, related_name="notifications")
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     seen = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return f"{self.user} {self.title}"
    
#     class Meta:
#         ordering = ["-created_at"]