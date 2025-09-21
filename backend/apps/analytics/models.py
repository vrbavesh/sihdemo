from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import User


class AnalyticsEvent(models.Model):
    """
    Track analytics events
    """
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('user_action', 'User Action'),
        ('api_call', 'API Call'),
        ('error', 'Error'),
        ('performance', 'Performance'),
    ]
    
    # Event details
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='analytics_events')
    
    # Generic foreign key for related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Event data
    properties = models.JSONField(default=dict, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"{self.event_name} - {self.created_at}"


class UserEngagement(models.Model):
    """
    Track user engagement metrics
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='engagement_metrics')
    
    # Engagement scores
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    activity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    social_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    contribution_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Activity metrics
    login_count = models.PositiveIntegerField(default=0)
    last_login = models.DateTimeField(blank=True, null=True)
    posts_created = models.PositiveIntegerField(default=0)
    comments_made = models.PositiveIntegerField(default=0)
    likes_given = models.PositiveIntegerField(default=0)
    connections_made = models.PositiveIntegerField(default=0)
    
    # Contribution metrics
    projects_created = models.PositiveIntegerField(default=0)
    projects_funded = models.PositiveIntegerField(default=0)
    total_contributed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mentorship_sessions = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_engagement'
    
    def __str__(self):
        return f"{self.user.username} - Engagement Score: {self.overall_score}"


class PlatformMetrics(models.Model):
    """
    Platform-wide metrics
    """
    date = models.DateField(unique=True)
    
    # User metrics
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    new_registrations = models.PositiveIntegerField(default=0)
    
    # Content metrics
    total_posts = models.PositiveIntegerField(default=0)
    total_projects = models.PositiveIntegerField(default=0)
    total_clubs = models.PositiveIntegerField(default=0)
    total_mentorships = models.PositiveIntegerField(default=0)
    
    # Engagement metrics
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    
    # Financial metrics
    total_funding_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_contributions = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    avg_page_load_time = models.DecimalField(max_digits=8, decimal_places=3, default=0.000)
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'platform_metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Platform Metrics - {self.date}"
