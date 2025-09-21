from rest_framework import serializers
from .models import *


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for user activities
    """
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description', 'metadata',
            'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'created_at'
        ]


class PageViewSerializer(serializers.ModelSerializer):
    """
    Serializer for page views
    """
    class Meta:
        model = PageView
        fields = [
            'id', 'user', 'page_url', 'page_title', 'session_id',
            'ip_address', 'user_agent', 'referrer', 'created_at'
        ]
        read_only_fields = [
            'id', 'created_at'
        ]


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for events
    """
    class Meta:
        model = Event
        fields = [
            'id', 'user', 'event_type', 'event_data', 'session_id',
            'ip_address', 'created_at'
        ]
        read_only_fields = [
            'id', 'created_at'
        ]


class UserEngagementSerializer(serializers.ModelSerializer):
    """
    Serializer for user engagement metrics
    """
    class Meta:
        model = UserEngagement
        fields = [
            'id', 'user', 'date', 'posts_created', 'comments_made',
            'likes_given', 'shares_made', 'connections_made',
            'time_spent_minutes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]