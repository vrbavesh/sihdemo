from rest_framework import serializers
from .models import Post, PostComment as Comment, PostLike as Like, PostShare as Share, PostBookmark as Bookmark, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    """
    Serializer for post images
    """
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'caption', 'order']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for posts
    """
    author = serializers.StringRelatedField(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'post_type', 'visibility',
            'likes_count', 'comments_count', 'shares_count', 'views_count',
            'project_upvotes', 'is_approved', 'is_featured', 'is_pinned',
            'created_at', 'updated_at', 'images', 'is_liked', 'is_bookmarked'
        ]
        read_only_fields = [
            'id', 'author', 'likes_count', 'comments_count', 'shares_count',
            'views_count', 'is_approved', 'is_featured', 'is_pinned',
            'created_at', 'updated_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating posts
    """
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'content', 'post_type', 'visibility', 'images'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        
        for i, image_data in enumerate(images_data):
            PostImage.objects.create(
                post=post,
                image=image_data,
                order=i
            )
        
        return post


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments
    """
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for likes
    """
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ShareSerializer(serializers.ModelSerializer):
    """
    Serializer for shares
    """
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Share
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for bookmarks
    """
    user = serializers.StringRelatedField(read_only=True)
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
