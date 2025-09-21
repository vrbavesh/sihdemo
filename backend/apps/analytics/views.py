from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import *
from .serializers import *


class UserActivityListView(generics.ListAPIView):
    """
    List user activities
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_type', 'user']
    search_fields = ['description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)


class UserActivityCreateView(generics.CreateAPIView):
    """
    Create user activity
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnalyticsDashboardView(APIView):
    """
    Get analytics dashboard data
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # User-specific analytics
        user_stats = {
            'total_posts': user.posts.count(),
            'total_projects': user.created_projects.count(),
            'total_connections': user.sent_connections.filter(status='accepted').count() + 
                               user.received_connections.filter(status='accepted').count(),
            'total_mentorship_requests': user.mentorship_requests_sent.count() + 
                                       user.mentorship_requests_received.count(),
        }
        
        # Activity analytics
        activity_stats = {
            'recent_activities': UserActivity.objects.filter(user=user)[:10].count(),
            'most_active_day': self.get_most_active_day(user),
        }
        
        return Response({
            'user_stats': user_stats,
            'activity_stats': activity_stats
        }, status=status.HTTP_200_OK)
    
    def get_most_active_day(self, user):
        # This would need more complex logic to determine the most active day
        return 'Monday'


class EngagementAnalyticsView(APIView):
    """
    Get engagement analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Post engagement
        total_likes = sum(post.likes_count for post in user.posts.all())
        total_comments = sum(post.comments_count for post in user.posts.all())
        total_shares = sum(post.shares_count for post in user.posts.all())
        
        engagement_stats = {
            'total_likes_received': total_likes,
            'total_comments_received': total_comments,
            'total_shares_received': total_shares,
            'average_engagement_per_post': (total_likes + total_comments + total_shares) / max(user.posts.count(), 1),
        }
        
        return Response(engagement_stats, status=status.HTTP_200_OK)


class ContentAnalyticsView(APIView):
    """
    Get content analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Content type distribution
        post_types = user.posts.values('post_type').annotate(count=Count('id'))
        
        content_stats = {
            'post_type_distribution': list(post_types),
            'most_popular_post_type': max(post_types, key=lambda x: x['count'])['post_type'] if post_types else None,
        }
        
        return Response(content_stats, status=status.HTTP_200_OK)


class NetworkAnalyticsView(APIView):
    """
    Get network analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Connection analytics
        sent_connections = user.sent_connections.filter(status='accepted').count()
        received_connections = user.received_connections.filter(status='accepted').count()
        
        network_stats = {
            'total_connections': sent_connections + received_connections,
            'sent_connections': sent_connections,
            'received_connections': received_connections,
            'connection_acceptance_rate': (received_connections / max(user.sent_connections.count(), 1)) * 100,
        }
        
        return Response(network_stats, status=status.HTTP_200_OK)