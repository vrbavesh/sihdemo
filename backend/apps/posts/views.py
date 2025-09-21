from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post, PostComment as Comment, PostLike as Like, PostShare as Share, PostBookmark as Bookmark, PostImage
from .serializers import (
    PostSerializer, PostCreateSerializer, CommentSerializer,
    LikeSerializer, ShareSerializer, BookmarkSerializer
)


class PostListView(generics.ListCreateAPIView):
    """
    List all posts or create a new post
    """
    queryset = Post.objects.select_related('author').prefetch_related('images', 'likes', 'comments')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_type', 'visibility', 'is_approved', 'is_featured']
    search_fields = ['content', 'author__first_name', 'author__last_name']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCreateView(generics.CreateAPIView):
    """
    Create a new post
    """
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post
    """
    queryset = Post.objects.select_related('author').prefetch_related('images', 'likes', 'comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated() and (self.get_object().author == self.request.user or self.request.user.is_staff)]
        return [permissions.IsAuthenticated()]


class PostLikeView(APIView):
    """
    Like or unlike a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            
            if not created:
                like.delete()
                post.likes_count = max(0, post.likes_count - 1)
                message = 'Post unliked'
            else:
                post.likes_count += 1
                message = 'Post liked'
            
            post.save()
            return Response({'message': message, 'liked': created}, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class PostCommentView(generics.ListCreateAPIView):
    """
    List comments for a post or create a new comment
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering = ['created_at']
    
    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id).select_related('author')
    
    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)


class PostShareView(APIView):
    """
    Share a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            share = Share.objects.create(user=request.user, post=post)
            post.shares_count += 1
            post.save()
            
            return Response({'message': 'Post shared'}, status=status.HTTP_201_CREATED)
        
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class PostBookmarkView(APIView):
    """
    Bookmark or unbookmark a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
            
            if not created:
                bookmark.delete()
                message = 'Post unbookmarked'
            else:
                message = 'Post bookmarked'
            
            return Response({'message': message, 'bookmarked': created}, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(id=self.kwargs['pk'])
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated() and (self.get_object().author == self.request.user or self.request.user.is_staff)]
        return [permissions.IsAuthenticated()]


class CommentLikeView(APIView):
    """
    Like or unlike a comment
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            # Note: You might want to create a CommentLike model for this
            return Response({'message': 'Comment liked'}, status=status.HTTP_200_OK)
        
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)


class UserPostsView(generics.ListAPIView):
    """
    List posts by a specific user
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_type', 'visibility']
    search_fields = ['content']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(author_id=user_id).select_related('author').prefetch_related('images', 'likes', 'comments')


class FeedView(generics.ListAPIView):
    """
    Get user's personalized feed
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_type']
    search_fields = ['content', 'author__first_name', 'author__last_name']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Get posts from user's connections and public posts
        user = self.request.user
        connections = user.sent_connections.filter(status='accepted').values_list('to_user', flat=True)
        connections |= user.received_connections.filter(status='accepted').values_list('from_user', flat=True)
        
        return Post.objects.filter(
            Q(author__in=connections) | Q(visibility='public')
        ).select_related('author').prefetch_related('images', 'likes', 'comments')