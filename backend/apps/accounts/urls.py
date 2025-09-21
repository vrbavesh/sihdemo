from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    
    # Profile Management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('update-last-active/', views.update_last_active, name='update-last-active'),
    path('stats/', views.user_stats, name='user-stats'),
    
    # User Discovery
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/search/', views.UserSearchView.as_view(), name='user-search'),
    
    # Connections
    path('connections/', views.UserConnectionView.as_view(), name='user-connections'),
    path('connections/request/<int:user_id>/', views.ConnectionRequestView.as_view(), name='connection-request'),
    path('connections/<int:connection_id>/respond/', views.ConnectionResponseView.as_view(), name='connection-response'),
    
    # Interests
    path('interests/', views.InterestListView.as_view(), name='interest-list'),
    path('user-interests/', views.UserInterestView.as_view(), name='user-interests'),
    
    # Activity
    path('activity/', views.UserActivityView.as_view(), name='user-activity'),
]
