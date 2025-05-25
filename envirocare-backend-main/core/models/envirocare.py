# Organisation model
from django.db import models
import uuid

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'
        ordering = ['created_at']

class Complaint(models.Model):
    SEVERITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.CharField(max_length=6, unique=True)
    description = models.TextField()
    location = models.TextField()
    notes = models.TextField(null=True, blank=True)
    affected_area = models.TextField(null=True, blank=True)
    environmental_impact = models.TextField(null=True, blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    is_resolved = models.BooleanField(default=False)
    reported_by_name = models.CharField(max_length=255)
    reported_by_number = models.CharField(max_length=20)
    resolved_date = models.DateTimeField(null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='complaints')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ref} - {self.description[:50]}"

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ref:
            # Generate a unique 6-character reference starting with REP
            import random
            import string
            while True:
                ref = 'REP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
                if not Complaint.objects.filter(ref=ref).exists():
                    self.ref = ref
                    break
        super().save(*args, **kwargs)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.CharField(max_length=6, null=True, blank=True)
    description = models.TextField()
    commented_by_name = models.CharField(max_length=255)
    commented_by_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commented_by_name} - {self.description[:50]}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

class Task(models.Model):
    SEVERITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    report_ref = models.CharField(max_length=6)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.report_ref} - {self.description[:50]}"

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']

# Signal to create task when complaint is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Complaint)
def create_task_from_complaint(sender, instance, created, **kwargs):
    if created:
        # Determine severity based on environmental impact
        severity = 'MEDIUM'  # default
        if instance.environmental_impact:
            impact_lower = instance.environmental_impact.lower()
            if any(word in impact_lower for word in ['severe', 'critical', 'high']):
                severity = 'HIGH'
            elif any(word in impact_lower for word in ['minor', 'low']):
                severity = 'LOW'

        Task.objects.create(
            organisation=instance.organisation,
            description=instance.description,
            report_ref=instance.ref,
            severity=severity
        )


OPENAI_API_KEY = 'sk--Mt3ou1jN98qIPTzBqbtdL5VEO2DPAxTjwMsKIBGExT3BlbkFJ4QCf6bydB0l85uXytT5e2PWS4li3PXGWo0UB4WEEEA'
