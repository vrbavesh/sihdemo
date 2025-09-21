from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Interest, UserInterest, UserConnection, UserActivity


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    interests = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'user_type', 'linkedin_profile', 'current_position', 'company',
            'graduation_year', 'department', 'phone_number', 'location',
            'bio', 'interests'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        interests_data = validated_data.pop('interests', [])
        
        user = User.objects.create_user(**validated_data)
        
        # Add interests
        for interest_name in interests_data:
            interest, created = Interest.objects.get_or_create(name=interest_name)
            UserInterest.objects.create(user=user, interest=interest)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs


class InterestSerializer(serializers.ModelSerializer):
    """
    Serializer for interests
    """
    class Meta:
        model = Interest
        fields = ['id', 'name', 'category', 'description']


class UserInterestSerializer(serializers.ModelSerializer):
    """
    Serializer for user interests
    """
    interest = InterestSerializer(read_only=True)
    interest_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserInterest
        fields = ['id', 'interest', 'interest_id', 'proficiency_level', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """
    interests = UserInterestSerializer(source='user_interests', many=True, read_only=True)
    connections_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'user_type', 'status',
            'linkedin_profile', 'current_position', 'company', 'graduation_year',
            'department', 'phone_number', 'location', 'bio', 'profile_picture',
            'cover_photo', 'is_verified', 'created_at', 'last_active',
            'interests', 'connections_count', 'posts_count', 'projects_count'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'is_verified']
    
    def get_connections_count(self, obj):
        return obj.sent_connections.filter(status='accepted').count() + \
               obj.received_connections.filter(status='accepted').count()
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    
    def get_projects_count(self, obj):
        return obj.created_projects.count()


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for user list (minimal data)
    """
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'user_type', 'current_position',
            'company', 'profile_picture', 'is_verified'
        ]


class UserConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for user connections
    """
    from_user = UserListSerializer(read_only=True)
    to_user = UserListSerializer(read_only=True)
    
    class Meta:
        model = UserConnection
        fields = [
            'id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for user activities
    """
    class Meta:
        model = UserActivity
        fields = [
            'id', 'activity_type', 'description', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class UserSearchSerializer(serializers.Serializer):
    """
    Serializer for user search
    """
    query = serializers.CharField(max_length=200)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, required=False)
    department = serializers.CharField(max_length=100, required=False)
    graduation_year = serializers.IntegerField(required=False)
    interests = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
