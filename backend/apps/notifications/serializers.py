from rest_framework import serializers
from .models import *


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'notification_type', 'title', 'message',
            'priority', 'is_read', 'is_sent', 'created_at', 'read_at'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'read_at'
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for notification preferences
    """
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'email_connection_requests', 'email_mentorship_requests',
            'email_project_updates', 'email_club_activities', 'email_system_updates',
            'push_connection_requests', 'push_mentorship_requests', 'push_post_interactions',
            'push_project_updates', 'push_club_activities', 'digest_frequency',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at'
        ]