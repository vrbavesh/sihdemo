from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, Interest, UserInterest, UserConnection, UserActivity
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserListSerializer, UserConnectionSerializer, UserActivitySerializer,
    PasswordChangeSerializer, UserSearchSerializer, InterestSerializer, UserInterestSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Update last active
        user.update_last_active()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile management
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    List users with filtering and search
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_type', 'department', 'graduation_year']
    search_fields = ['first_name', 'last_name', 'company', 'current_position']
    ordering_fields = ['first_name', 'last_name', 'created_at', 'last_active']
    ordering = ['-last_active']
    
    def get_queryset(self):
        return User.objects.filter(status='active').exclude(id=self.request.user.id)


class UserSearchView(APIView):
    """
    Advanced user search
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = UserSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        query = data.get('query', '')
        user_type = data.get('user_type')
        department = data.get('department')
        graduation_year = data.get('graduation_year')
        interests = data.get('interests', [])
        
        # Build query
        q = Q(status='active')
        
        if query:
            q &= (
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(company__icontains=query) |
                Q(current_position__icontains=query)
            )
        
        if user_type:
            q &= Q(user_type=user_type)
        
        if department:
            q &= Q(department__icontains=department)
        
        if graduation_year:
            q &= Q(graduation_year=graduation_year)
        
        if interests:
            q &= Q(user_interests__interest__name__in=interests)
        
        users = User.objects.filter(q).distinct().exclude(id=request.user.id)
        
        return Response({
            'users': UserListSerializer(users, many=True).data,
            'count': users.count()
        })


class UserConnectionView(generics.ListCreateAPIView):
    """
    User connections management
    """
    serializer_class = UserConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserConnection.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        ).filter(status='accepted')
    
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class ConnectionRequestView(APIView):
    """
    Send connection request
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if target_user == request.user:
            return Response({'error': 'Cannot connect to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if connection already exists
        connection, created = UserConnection.objects.get_or_create(
            from_user=request.user,
            to_user=target_user,
            defaults={'status': 'pending'}
        )
        
        if not created:
            return Response({'error': 'Connection request already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Connection request sent'}, status=status.HTTP_201_CREATED)


class ConnectionResponseView(APIView):
    """
    Accept or reject connection request
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, connection_id):
        try:
            connection = UserConnection.objects.get(
                id=connection_id,
                to_user=request.user,
                status='pending'
            )
        except UserConnection.DoesNotExist:
            return Response({'error': 'Connection request not found'}, status=status.HTTP_404_NOT_FOUND)
        
        action = request.data.get('action')
        if action == 'accept':
            connection.status = 'accepted'
            connection.save()
            return Response({'message': 'Connection request accepted'})
        elif action == 'reject':
            connection.status = 'rejected'
            connection.save()
            return Response({'message': 'Connection request rejected'})
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


class InterestListView(generics.ListAPIView):
    """
    List all interests
    """
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'category']


class UserInterestView(generics.ListCreateAPIView):
    """
    Manage user interests
    """
    serializer_class = UserInterestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PasswordChangeView(APIView):
    """
    Change user password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})


class UserActivityView(generics.ListAPIView):
    """
    Get user activity feed
    """
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_last_active(request):
    """
    Update user's last active timestamp
    """
    request.user.update_last_active()
    return Response({'message': 'Last active updated'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    Get user statistics
    """
    user = request.user
    
    stats = {
        'connections_count': user.sent_connections.filter(status='accepted').count() + 
                           user.received_connections.filter(status='accepted').count(),
        'posts_count': user.posts.count(),
        'projects_count': user.created_projects.count(),
        'mentorship_requests_count': user.mentorship_requests.count(),
        'club_memberships_count': user.club_memberships.filter(status='active').count(),
        'contributions_count': user.contributions.count(),
    }
    
    return Response(stats)
