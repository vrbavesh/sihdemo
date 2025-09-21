from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from apps.accounts.models import User


class Post(models.Model):
    """
    Social media posts and updates
    """
    POST_TYPES = [
        ('general', 'General'),
        ('achievement', 'Achievement'),
        ('project', 'Project'),
        ('research', 'Research'),
        ('job_opportunity', 'Job Opportunity'),
        ('event', 'Event'),
        ('mentorship', 'Mentorship'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('connections', 'Connections Only'),
        ('department', 'Department Only'),
        ('private', 'Private'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    
    # Engagement metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Project-specific fields
    project_upvotes = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'post_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_approved', 'visibility']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}..."


class PostImage(models.Model):
    """
    Images attached to posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_images'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.post.id} - Image {self.order}"


class PostLike(models.Model):
    """
    Post likes/reactions
    """
    REACTION_TYPES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('laugh', 'Laugh'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_likes'
        unique_together = ['user', 'post']
        indexes = [
            models.Index(fields=['post', 'reaction_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} {self.reaction_type}s {self.post.id}"


class PostComment(models.Model):
    """
    Comments on posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    likes_count = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"{self.author.username} commented on {self.post.id}"


class PostBookmark(models.Model):
    """
    User bookmarks for posts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_bookmarks'
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.id}"


class PostShare(models.Model):
    """
    Post sharing tracking
    """
    SHARE_TYPES = [
        ('internal', 'Internal Share'),
        ('external', 'External Share'),
        ('social', 'Social Media'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_shares')
    share_type = models.CharField(max_length=20, choices=SHARE_TYPES, default='internal')
    platform = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_shares'
        indexes = [
            models.Index(fields=['post', 'share_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} shared {self.post.id}"


class PostView(models.Model):
    """
    Track post views for analytics
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_views', blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'post_views'
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]
    
    def __str__(self):
        return f"View of {self.post.id} by {self.user or self.ip_address}"
