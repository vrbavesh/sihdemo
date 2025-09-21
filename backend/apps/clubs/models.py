from django.db import models
from django.utils import timezone
from apps.accounts.models import User


class Club(models.Model):
    """
    Clubs and communities
    """
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('invite_only', 'Invite Only'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Approval'),
    ]
    
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('arts', 'Arts & Culture'),
        ('sports', 'Sports'),
        ('academic', 'Academic'),
        ('professional', 'Professional'),
        ('social', 'Social'),
        ('environmental', 'Environmental'),
        ('healthcare', 'Healthcare'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Ownership and Management
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_clubs')
    moderators = models.ManyToManyField(User, related_name='moderated_clubs', blank=True)
    
    # Settings
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    
    # Media
    cover_image = models.ImageField(upload_to='club_covers/', blank=True, null=True)
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    
    # Metrics
    members_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    events_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'clubs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'visibility']),
            models.Index(fields=['category']),
            models.Index(fields=['owner']),
            models.Index(fields=['last_activity']),
        ]
    
    def __str__(self):
        return self.name


class ClubMembership(models.Model):
    """
    Club membership relationships
    """
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('banned', 'Banned'),
    ]
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Invitation details
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='sent_invitations')
    invitation_message = models.TextField(blank=True)
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'club_memberships'
        unique_together = ['club', 'user']
        indexes = [
            models.Index(fields=['club', 'status']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.club.name} ({self.role})"


class ClubPost(models.Model):
    """
    Posts within clubs
    """
    POST_TYPES = [
        ('general', 'General'),
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('discussion', 'Discussion'),
        ('resource', 'Resource'),
    ]
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    
    # Engagement
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Moderation
    is_pinned = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'club_posts'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['club', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['post_type']),
        ]
    
    def __str__(self):
        return f"{self.club.name} - {self.title or self.content[:50]}"


class ClubEvent(models.Model):
    """
    Events organized by clubs
    """
    EVENT_TYPES = [
        ('meeting', 'Meeting'),
        ('workshop', 'Workshop'),
        ('social', 'Social'),
        ('conference', 'Conference'),
        ('networking', 'Networking'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    
    # Event details
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meeting')
    
    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Location
    location_type = models.CharField(max_length=20, choices=[
        ('physical', 'Physical Location'),
        ('virtual', 'Virtual'),
        ('hybrid', 'Hybrid'),
    ], default='virtual')
    location = models.CharField(max_length=200, blank=True)
    meeting_link = models.URLField(blank=True)
    
    # Registration
    max_attendees = models.PositiveIntegerField(blank=True, null=True)
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_public = models.BooleanField(default=True)
    
    # Metrics
    attendees_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'club_events'
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['club', 'start_date']),
            models.Index(fields=['organizer']),
            models.Index(fields=['status', 'is_public']),
        ]
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"


class EventRegistration(models.Model):
    """
    Event registrations
    """
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]
    
    event = models.ForeignKey(ClubEvent, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    
    # Additional information
    notes = models.TextField(blank=True)
    dietary_requirements = models.TextField(blank=True)
    
    # Timestamps
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_registrations'
        unique_together = ['event', 'user']
        indexes = [
            models.Index(fields=['event', 'status']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.event.title}"


class ClubDiscussion(models.Model):
    """
    Discussion threads within clubs
    """
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Threading
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    
    # Engagement
    likes_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Moderation
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reply_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'club_discussions'
        ordering = ['-is_pinned', '-last_reply_at']
        indexes = [
            models.Index(fields=['club', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"


class ClubResource(models.Model):
    """
    Resources shared within clubs
    """
    RESOURCE_TYPES = [
        ('document', 'Document'),
        ('link', 'Link'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='resources')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    
    # Resource details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    
    # File information
    file = models.FileField(upload_to='club_resources/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    
    # Access control
    is_public = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'club_resources'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['club', 'resource_type']),
            models.Index(fields=['uploaded_by']),
        ]
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"
