from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Project, Contribution
from .serializers import ProjectSerializer, ProjectCreateSerializer, ContributionSerializer


class ProjectListView(generics.ListCreateAPIView):
    """
    List all projects or create a new project
    """
    queryset = Project.objects.select_related('creator').prefetch_related('contributions')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'is_verified', 'is_featured']
    search_fields = ['title', 'description', 'creator__first_name', 'creator__last_name']
    ordering_fields = ['created_at', 'target_amount', 'current_amount', 'backers_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProjectCreateView(generics.CreateAPIView):
    """
    Create a new project
    """
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project
    """
    queryset = Project.objects.select_related('creator').prefetch_related('contributions')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated() and (self.get_object().creator == self.request.user or self.request.user.is_staff)]
        return [permissions.IsAuthenticated()]


class ProjectLikeView(APIView):
    """
    Like or unlike a project
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            # Note: You might want to create a ProjectLike model for this
            project.likes_count += 1
            project.save()
            return Response({'message': 'Project liked'}, status=status.HTTP_200_OK)
        
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class ProjectShareView(APIView):
    """
    Share a project
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            project.shares_count += 1
            project.save()
            return Response({'message': 'Project shared'}, status=status.HTTP_200_OK)
        
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class ContributionCreateView(APIView):
    """
    Contribute to a project
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            amount = request.data.get('amount')
            is_anonymous = request.data.get('is_anonymous', False)
            
            if not amount or amount <= 0:
                return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
            
            if project.status != 'active':
                return Response({'error': 'Project is not active'}, status=status.HTTP_400_BAD_REQUEST)
            
            contribution = Contribution.objects.create(
                project=project,
                contributor=request.user,
                amount=amount,
                is_anonymous=is_anonymous
            )
            
            # Update project funding
            project.current_amount += amount
            project.backers_count += 1
            project.save()
            
            return Response(ContributionSerializer(contribution).data, status=status.HTTP_201_CREATED)
        
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class ContributionListView(generics.ListAPIView):
    """
    List contributions for a project
    """
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Contribution.objects.filter(contributor=self.request.user).select_related('project', 'contributor')


class ProjectUpdateListView(generics.ListCreateAPIView):
    """
    List project updates or create a new update
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # This would need a ProjectUpdate model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Project updates feature coming soon'}, status=status.HTTP_200_OK)


class ProjectUpdateCreateView(generics.CreateAPIView):
    """
    Create a project update
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Project updates feature coming soon'}, status=status.HTTP_200_OK)


class RefundListView(generics.ListAPIView):
    """
    List refunds
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # This would need a Refund model
        return []
    
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Refunds feature coming soon'}, status=status.HTTP_200_OK)


class RefundDetailView(generics.RetrieveAPIView):
    """
    Retrieve a refund
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Refunds feature coming soon'}, status=status.HTTP_200_OK)


class CrowdfundingStatsView(APIView):
    """
    Get crowdfunding statistics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        stats = {
            'total_projects': Project.objects.count(),
            'active_projects': Project.objects.filter(status='active').count(),
            'total_raised': sum(p.current_amount for p in Project.objects.all()),
            'total_contributions': Contribution.objects.count(),
        }
        return Response(stats, status=status.HTTP_200_OK)


class UserProjectsView(generics.ListAPIView):
    """
    List projects by a specific user
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'target_amount', 'current_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Project.objects.filter(creator_id=user_id).select_related('creator').prefetch_related('contributions')


class FeaturedProjectsView(generics.ListAPIView):
    """
    List featured projects
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'target_amount', 'current_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Project.objects.filter(
            is_featured=True,
            status='active'
        ).select_related('creator').prefetch_related('contributions')