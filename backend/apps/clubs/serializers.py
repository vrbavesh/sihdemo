from rest_framework import serializers
from .models import *


class ClubSerializer(serializers.ModelSerializer):
    """
    Serializer for clubs
    """
    owner = serializers.StringRelatedField(read_only=True)
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = [
            'id', 'name', 'description', 'short_description', 'owner',
            'category', 'visibility', 'status', 'is_verified', 'cover_image',
            'logo', 'members_count', 'posts_count', 'events_count',
            'created_at', 'updated_at', 'last_activity', 'is_member'
        ]
        read_only_fields = [
            'id', 'owner', 'members_count', 'posts_count', 'events_count',
            'is_verified', 'created_at', 'updated_at', 'last_activity'
        ]
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(user=request.user).exists()
        return False


class ClubCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating clubs
    """
    class Meta:
        model = Club
        fields = [
            'name', 'description', 'short_description', 'category',
            'visibility', 'cover_image', 'logo'
        ]


class ClubMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for club memberships
    """
    user = serializers.StringRelatedField(read_only=True)
    club = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ClubMembership
        fields = [
            'id', 'club', 'user', 'role', 'joined_at', 'is_active'
        ]
        read_only_fields = ['id', 'joined_at']


class ClubEventSerializer(serializers.ModelSerializer):
    """
    Serializer for club events
    """
    organizer = serializers.StringRelatedField(read_only=True)
    club = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ClubEvent
        fields = [
            'id', 'club', 'title', 'description', 'event_date',
            'location', 'organizer', 'max_attendees', 'attendees_count',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'organizer', 'club', 'attendees_count',
            'created_at', 'updated_at'
        ]


class ClubPostSerializer(serializers.ModelSerializer):
    """
    Serializer for club posts
    """
    author = serializers.StringRelatedField(read_only=True)
    club = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ClubPost
        fields = [
            'id', 'club', 'author', 'title', 'content', 'post_type',
            'is_pinned', 'likes_count', 'comments_count', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'club', 'likes_count', 'comments_count',
            'created_at', 'updated_at'
        ]