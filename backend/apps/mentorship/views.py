from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import *
from .serializers import *


class MentorshipProgramListView(generics.ListCreateAPIView):
    """
    List mentorship programs or create a new program
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        # This would need a MentorshipProgram model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Mentorship programs feature coming soon'}, status=status.HTTP_200_OK)


class MentorshipProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a mentorship program
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Mentorship programs feature coming soon'}, status=status.HTTP_200_OK)


class MentorProfileListView(generics.ListAPIView):
    """
    List mentor profiles
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['expertise_areas', 'availability_status', 'is_verified']
    search_fields = ['bio', 'expertise_areas', 'user__first_name', 'user__last_name']
    ordering_fields = ['rating', 'total_mentees', 'created_at']
    ordering = ['-rating']
    
    def get_queryset(self):
        return MentorProfile.objects.filter(is_active=True).select_related('user')


class MentorProfileDetailView(generics.RetrieveAPIView):
    """
    Retrieve a mentor profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MentorProfile.objects.filter(is_active=True).select_related('user')


class MentorProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update current user's mentor profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return MentorProfile.objects.get_or_create(user=self.request.user)[0]


class MentorshipRequestListView(generics.ListCreateAPIView):
    """
    List mentorship requests or create a new request
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'mentor']
    search_fields = ['subject', 'message', 'goals']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        return MentorshipRequest.objects.filter(
            Q(mentee=user) | Q(mentor=user)
        ).select_related('mentee', 'mentor')


class MentorshipRequestCreateView(generics.CreateAPIView):
    """
    Create a new mentorship request
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(mentee=self.request.user)


class MentorshipRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a mentorship request
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return MentorshipRequest.objects.filter(
            Q(mentee=user) | Q(mentor=user)
        ).select_related('mentee', 'mentor')


class MentorshipRequestResponseView(APIView):
    """
    Respond to a mentorship request
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            mentorship_request = MentorshipRequest.objects.get(id=pk, mentor=request.user)
            action = request.data.get('action')  # 'accept' or 'reject'
            response_message = request.data.get('message', '')
            
            if action == 'accept':
                mentorship_request.status = 'accepted'
                mentorship_request.mentor_response = response_message
            elif action == 'reject':
                mentorship_request.status = 'rejected'
                mentorship_request.rejection_reason = response_message
            
            mentorship_request.save()
            return Response({'message': f'Request {action}ed'}, status=status.HTTP_200_OK)
        
        except MentorshipRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)


class MentorshipSessionListView(generics.ListCreateAPIView):
    """
    List mentorship sessions or create a new session
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'mentor', 'mentee']
    ordering_fields = ['scheduled_at', 'created_at']
    ordering = ['-scheduled_at']
    
    def get_queryset(self):
        user = self.request.user
        return MentorshipSession.objects.filter(
            Q(mentor=user) | Q(mentee=user)
        ).select_related('mentor', 'mentee', 'request')


class MentorshipSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a mentorship session
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return MentorshipSession.objects.filter(
            Q(mentor=user) | Q(mentee=user)
        ).select_related('mentor', 'mentee', 'request')


class SessionStartView(APIView):
    """
    Start a mentorship session
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            session = MentorshipSession.objects.get(id=pk)
            if session.mentor != request.user and session.mentee != request.user:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
            session.status = 'in_progress'
            session.save()
            return Response({'message': 'Session started'}, status=status.HTTP_200_OK)
        
        except MentorshipSession.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


class SessionEndView(APIView):
    """
    End a mentorship session
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            session = MentorshipSession.objects.get(id=pk)
            if session.mentor != request.user and session.mentee != request.user:
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
            session.status = 'completed'
            session.save()
            return Response({'message': 'Session ended'}, status=status.HTTP_200_OK)
        
        except MentorshipSession.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


class MentorshipFeedbackListView(generics.ListCreateAPIView):
    """
    List mentorship feedback or create new feedback
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        # This would need a MentorshipFeedback model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Mentorship feedback feature coming soon'}, status=status.HTTP_200_OK)


class MentorshipFeedbackCreateView(generics.CreateAPIView):
    """
    Create mentorship feedback
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Mentorship feedback feature coming soon'}, status=status.HTTP_200_OK)


class MentorshipGoalListView(generics.ListCreateAPIView):
    """
    List mentorship goals or create new goals
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        # This would need a MentorshipGoal model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Mentorship goals feature coming soon'}, status=status.HTTP_200_OK)


class MentorshipGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a mentorship goal
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Mentorship goals feature coming soon'}, status=status.HTTP_200_OK)