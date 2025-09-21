from rest_framework import serializers
from .models import *


class MentorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for mentor profiles
    """
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user', 'bio', 'expertise_areas', 'years_of_experience',
            'current_company', 'current_position', 'availability_status',
            'max_mentees', 'preferred_meeting_times', 'timezone',
            'preferred_mentee_types', 'mentoring_goals', 'total_mentees',
            'rating', 'total_sessions', 'is_verified', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'total_mentees', 'rating', 'total_sessions',
            'is_verified', 'created_at', 'updated_at'
        ]


class MentorshipRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for mentorship requests
    """
    mentee = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = MentorshipRequest
        fields = [
            'id', 'mentee', 'mentor', 'program', 'subject', 'message',
            'goals', 'preferred_meeting_frequency', 'expected_duration',
            'status', 'mentor_response', 'rejection_reason', 'created_at',
            'updated_at', 'responded_at', 'started_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'mentee', 'created_at', 'updated_at', 'responded_at',
            'started_at', 'completed_at'
        ]


class MentorshipSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for mentorship sessions
    """
    mentor = serializers.StringRelatedField(read_only=True)
    mentee = serializers.StringRelatedField(read_only=True)
    request = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = MentorshipSession
        fields = [
            'id', 'request', 'mentor', 'mentee', 'scheduled_at',
            'duration_minutes', 'meeting_link', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]


class MentorshipProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for mentorship programs
    """
    class Meta:
        model = MentorshipProgram
        fields = [
            'id', 'name', 'description', 'duration_weeks', 'max_participants',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]


class MentorshipFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for mentorship feedback
    """
    class Meta:
        model = MentorshipFeedback
        fields = [
            'id', 'session', 'mentor', 'mentee', 'rating', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]


class MentorshipGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for mentorship goals
    """
    class Meta:
        model = MentorshipGoal
        fields = [
            'id', 'request', 'title', 'description', 'target_date',
            'is_completed', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]