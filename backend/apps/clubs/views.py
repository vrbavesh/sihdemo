from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import *
from .serializers import *


class ClubListView(generics.ListCreateAPIView):
    """
    List clubs or create a new club
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'visibility', 'status', 'is_verified']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['created_at', 'members_count', 'posts_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Club.objects.filter(status='active').select_related('owner').prefetch_related('members')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClubCreateSerializer
        return ClubSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ClubCreateView(generics.CreateAPIView):
    """
    Create a new club
    """
    serializer_class = ClubCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ClubDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a club
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Club.objects.select_related('owner').prefetch_related('members')
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated() and (self.get_object().owner == self.request.user or self.request.user.is_staff)]
        return [permissions.IsAuthenticated()]


class ClubJoinView(APIView):
    """
    Join a club
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            club = Club.objects.get(id=pk)
            membership, created = ClubMembership.objects.get_or_create(
                club=club,
                user=request.user,
                defaults={'role': 'member'}
            )
            
            if created:
                club.members_count += 1
                club.save()
                return Response({'message': 'Joined club successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Already a member'}, status=status.HTTP_200_OK)
        
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)


class ClubLeaveView(APIView):
    """
    Leave a club
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            club = Club.objects.get(id=pk)
            membership = ClubMembership.objects.filter(club=club, user=request.user).first()
            
            if membership:
                membership.delete()
                club.members_count = max(0, club.members_count - 1)
                club.save()
                return Response({'message': 'Left club successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Not a member of this club'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Club.DoesNotExist:
            return Response({'error': 'Club not found'}, status=status.HTTP_404_NOT_FOUND)


class ClubPostListView(generics.ListCreateAPIView):
    """
    List club posts or create a new post
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        club_id = self.kwargs['pk']
        return ClubPost.objects.filter(club_id=club_id).select_related('author')
    
    def perform_create(self, serializer):
        club_id = self.kwargs['pk']
        serializer.save(author=self.request.user, club_id=club_id)


class ClubPostCreateView(generics.CreateAPIView):
    """
    Create a new club post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        club_id = self.kwargs['pk']
        serializer.save(author=self.request.user, club_id=club_id)


class ClubEventListView(generics.ListCreateAPIView):
    """
    List club events or create a new event
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-event_date']
    
    def get_queryset(self):
        club_id = self.kwargs['pk']
        return ClubEvent.objects.filter(club_id=club_id).select_related('organizer')
    
    def perform_create(self, serializer):
        club_id = self.kwargs['pk']
        serializer.save(organizer=self.request.user, club_id=club_id)


class ClubEventCreateView(generics.CreateAPIView):
    """
    Create a new club event
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        club_id = self.kwargs['pk']
        serializer.save(organizer=self.request.user, club_id=club_id)


class ClubEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a club event
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ClubEvent.objects.select_related('organizer', 'club')


class EventRegistrationView(APIView):
    """
    Register for a club event
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            event = ClubEvent.objects.get(id=pk)
            # This would need an EventRegistration model
            return Response({'message': 'Event registration feature coming soon'}, status=status.HTTP_200_OK)
        
        except ClubEvent.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


class ClubDiscussionListView(generics.ListCreateAPIView):
    """
    List club discussions or create a new discussion
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        # This would need a ClubDiscussion model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Club discussions feature coming soon'}, status=status.HTTP_200_OK)


class ClubDiscussionCreateView(generics.CreateAPIView):
    """
    Create a new club discussion
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Club discussions feature coming soon'}, status=status.HTTP_200_OK)


class ClubDiscussionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a club discussion
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Club discussions feature coming soon'}, status=status.HTTP_200_OK)


class ClubResourceListView(generics.ListAPIView):
    """
    List club resources
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        # This would need a ClubResource model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Club resources feature coming soon'}, status=status.HTTP_200_OK)


class ClubResourceUploadView(generics.CreateAPIView):
    """
    Upload a club resource
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Club resources feature coming soon'}, status=status.HTTP_200_OK)


class ClubMembersView(generics.ListAPIView):
    """
    List club members
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['joined_at']
    
    def get_queryset(self):
        club_id = self.kwargs['pk']
        return ClubMembership.objects.filter(club_id=club_id).select_related('user')


class UserClubsView(generics.ListAPIView):
    """
    List user's clubs
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-joined_at']
    
    def get_queryset(self):
        return ClubMembership.objects.filter(user=self.request.user).select_related('club', 'user')