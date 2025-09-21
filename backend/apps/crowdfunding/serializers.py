from rest_framework import serializers
from .models import Project, Contribution


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for projects
    """
    creator = serializers.StringRelatedField(read_only=True)
    funding_percentage = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    is_funded = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'short_description', 'creator',
            'category', 'target_amount', 'current_amount', 'currency',
            'start_date', 'end_date', 'duration_days', 'status',
            'is_verified', 'is_featured', 'backers_count', 'views_count',
            'likes_count', 'shares_count', 'cover_image', 'created_at',
            'updated_at', 'funding_percentage', 'days_remaining',
            'is_funded', 'is_expired'
        ]
        read_only_fields = [
            'id', 'creator', 'current_amount', 'backers_count',
            'views_count', 'likes_count', 'shares_count', 'is_verified',
            'is_featured', 'created_at', 'updated_at'
        ]
    
    def get_funding_percentage(self, obj):
        if obj.target_amount > 0:
            return min((obj.current_amount / obj.target_amount) * 100, 100)
        return 0
    
    def get_days_remaining(self, obj):
        from django.utils import timezone
        if obj.end_date:
            delta = obj.end_date - timezone.now().date()
            return max(0, delta.days)
        return 0
    
    def get_is_funded(self, obj):
        return obj.current_amount >= obj.target_amount
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.end_date and obj.end_date < timezone.now().date()


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating projects
    """
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'short_description', 'category',
            'target_amount', 'currency', 'duration_days', 'cover_image'
        ]
    
    def create(self, validated_data):
        from datetime import timedelta
        from django.utils import timezone
        
        # Set start and end dates
        validated_data['start_date'] = timezone.now().date()
        validated_data['end_date'] = validated_data['start_date'] + timedelta(days=validated_data['duration_days'])
        
        return Project.objects.create(**validated_data)


class ContributionSerializer(serializers.ModelSerializer):
    """
    Serializer for contributions
    """
    contributor = serializers.StringRelatedField(read_only=True)
    project = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Contribution
        fields = [
            'id', 'project', 'contributor', 'amount', 'contribution_type',
            'payment_status', 'is_anonymous', 'display_name', 'created_at'
        ]
        read_only_fields = ['id', 'contributor', 'project', 'created_at']
