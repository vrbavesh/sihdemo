from django.db import models
from django.utils import timezone
from decimal import Decimal
from apps.accounts.models import User


class Project(models.Model):
    """
    Crowdfunding projects
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('funded', 'Fully Funded'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]
    
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('environment', 'Environment'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('arts', 'Arts & Culture'),
        ('community', 'Community'),
        ('research', 'Research'),
        ('social_impact', 'Social Impact'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Funding Information
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='USD')
    
    # Timeline
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_days = models.PositiveIntegerField()
    
    # Status and Moderation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)
    
    # Metrics
    backers_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Media
    cover_image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['creator']),
            models.Index(fields=['end_date']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def funding_percentage(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0
    
    @property
    def days_remaining(self):
        if self.status == 'active':
            delta = self.end_date - timezone.now()
            return max(0, delta.days)
        return 0
    
    @property
    def is_funded(self):
        return self.current_amount >= self.target_amount
    
    @property
    def is_expired(self):
        return timezone.now() > self.end_date and self.status == 'active'


class ProjectImage(models.Model):
    """
    Additional images for projects
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'project_images'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


class ProjectUpdate(models.Model):
    """
    Project updates and milestones
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'project_updates'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"


class Contribution(models.Model):
    """
    User contributions to projects
    """
    CONTRIBUTION_TYPES = [
        ('one_time', 'One-time'),
        ('recurring', 'Recurring'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributions')
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES, default='one_time')
    
    # Payment Information
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Anonymity
    is_anonymous = models.BooleanField(default=False)
    display_name = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contributions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['contributor']),
            models.Index(fields=['payment_status']),
        ]
    
    def __str__(self):
        return f"{self.contributor.username} contributed ${self.amount} to {self.project.title}"


class ProjectLike(models.Model):
    """
    User likes for projects
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'project_likes'
        unique_together = ['project', 'user']
    
    def __str__(self):
        return f"{self.user.username} likes {self.project.title}"


class ProjectShare(models.Model):
    """
    Project sharing tracking
    """
    SHARE_PLATFORMS = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('email', 'Email'),
        ('copy_link', 'Copy Link'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_shares')
    platform = models.CharField(max_length=20, choices=SHARE_PLATFORMS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'project_shares'
        indexes = [
            models.Index(fields=['project', 'platform']),
        ]
    
    def __str__(self):
        return f"{self.user.username} shared {self.project.title} on {self.platform}"


class ProjectView(models.Model):
    """
    Track project views for analytics
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_views', blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'project_views'
        indexes = [
            models.Index(fields=['project', 'created_at']),
        ]
    
    def __str__(self):
        return f"View of {self.project.title} by {self.user or self.ip_address}"


class Refund(models.Model):
    """
    Refund requests and processing
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]
    
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    stripe_refund_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'refunds'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund for {self.contribution} - ${self.amount}"
