from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import User


class Notification(models.Model):
    """
    User notifications
    """
    NOTIFICATION_TYPES = [
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('post_liked', 'Post Liked'),
        ('post_commented', 'Post Commented'),
        ('post_shared', 'Post Shared'),
        ('project_funded', 'Project Funded'),
        ('mentorship_request', 'Mentorship Request'),
        ('mentorship_accepted', 'Mentorship Accepted'),
        ('club_invitation', 'Club Invitation'),
        ('event_reminder', 'Event Reminder'),
        ('system', 'System Notification'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Recipient
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Notification details
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Generic foreign key for related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationPreference(models.Model):
    """
    User notification preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email notifications
    email_connection_requests = models.BooleanField(default=True)
    email_mentorship_requests = models.BooleanField(default=True)
    email_project_updates = models.BooleanField(default=True)
    email_club_activities = models.BooleanField(default=True)
    email_system_updates = models.BooleanField(default=True)
    
    # Push notifications
    push_connection_requests = models.BooleanField(default=True)
    push_mentorship_requests = models.BooleanField(default=True)
    push_post_interactions = models.BooleanField(default=True)
    push_project_updates = models.BooleanField(default=True)
    push_club_activities = models.BooleanField(default=True)
    
    # Frequency
    digest_frequency = models.CharField(max_length=20, choices=[
        ('immediate', 'Immediate'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('never', 'Never'),
    ], default='daily')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"{self.user.username} - Notification Preferences"
