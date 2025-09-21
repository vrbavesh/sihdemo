from django.db import models
from django.utils import timezone
from apps.accounts.models import User


class MentorshipProgram(models.Model):
    """
    Mentorship programs and initiatives
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=100, blank=True)
    target_audience = models.CharField(max_length=200, blank=True)
    duration_weeks = models.PositiveIntegerField(default=12)
    max_mentees_per_mentor = models.PositiveIntegerField(default=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_programs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mentorship_programs'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class MentorProfile(models.Model):
    """
    Mentor profiles and availability
    """
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField()
    expertise_areas = models.TextField(help_text="Comma-separated list of expertise areas")
    years_of_experience = models.PositiveIntegerField()
    current_company = models.CharField(max_length=200, blank=True)
    current_position = models.CharField(max_length=200, blank=True)
    
    # Availability
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    max_mentees = models.PositiveIntegerField(default=3)
    preferred_meeting_times = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Preferences
    preferred_mentee_types = models.CharField(max_length=200, blank=True)
    mentoring_goals = models.TextField(blank=True)
    
    # Metrics
    total_mentees = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_sessions = models.PositiveIntegerField(default=0)
    
    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mentor_profiles'
        indexes = [
            models.Index(fields=['availability_status', 'is_active']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - Mentor"


class MentorshipRequest(models.Model):
    """
    Mentorship requests from mentees to mentors
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_requests')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_mentorship_requests')
    program = models.ForeignKey(MentorshipProgram, on_delete=models.CASCADE, related_name='requests', blank=True, null=True)
    
    # Request details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    goals = models.TextField(help_text="What the mentee hopes to achieve")
    preferred_meeting_frequency = models.CharField(max_length=50, blank=True)
    expected_duration = models.CharField(max_length=50, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mentor_response = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'mentorship_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mentor', 'status']),
            models.Index(fields=['mentee', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.mentee.full_name} -> {self.mentor.full_name}"


class MentorshipSession(models.Model):
    """
    Individual mentorship sessions
    """
    SESSION_TYPES = [
        ('video_call', 'Video Call'),
        ('phone_call', 'Phone Call'),
        ('in_person', 'In Person'),
        ('chat', 'Chat'),
        ('email', 'Email'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    mentorship = models.ForeignKey(MentorshipRequest, on_delete=models.CASCADE, related_name='sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Scheduling
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    meeting_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    actual_duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    
    # Notes and feedback
    mentor_notes = models.TextField(blank=True)
    mentee_notes = models.TextField(blank=True)
    action_items = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'mentorship_sessions'
        ordering = ['scheduled_at']
        indexes = [
            models.Index(fields=['mentorship', 'scheduled_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.mentorship} - {self.title}"


class MentorshipFeedback(models.Model):
    """
    Feedback between mentors and mentees
    """
    FEEDBACK_TYPES = [
        ('mentor_to_mentee', 'Mentor to Mentee'),
        ('mentee_to_mentor', 'Mentee to Mentor'),
    ]
    
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    
    mentorship = models.ForeignKey(MentorshipRequest, on_delete=models.CASCADE, related_name='feedback')
    session = models.ForeignKey(MentorshipSession, on_delete=models.CASCADE, related_name='feedback', blank=True, null=True)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedback')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedback')
    
    # Ratings
    communication_rating = models.IntegerField(choices=RATING_CHOICES)
    helpfulness_rating = models.IntegerField(choices=RATING_CHOICES)
    professionalism_rating = models.IntegerField(choices=RATING_CHOICES)
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    
    # Written feedback
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    additional_comments = models.TextField(blank=True)
    
    # Anonymity
    is_anonymous = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mentorship_feedback'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mentorship', 'feedback_type']),
            models.Index(fields=['to_user', 'overall_rating']),
        ]
    
    def __str__(self):
        return f"{self.from_user.full_name} -> {self.to_user.full_name} ({self.overall_rating}/5)"


class MentorshipGoal(models.Model):
    """
    Goals and milestones for mentorship relationships
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    mentorship = models.ForeignKey(MentorshipRequest, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress_notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_goals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'mentorship_goals'
        ordering = ['target_date', 'created_at']
    
    def __str__(self):
        return f"{self.mentorship} - {self.title}"
