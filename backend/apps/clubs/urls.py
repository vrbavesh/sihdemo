from django.urls import path
from . import views

urlpatterns = [
    # Clubs
    path('', views.ClubListView.as_view(), name='club-list'),
    path('create/', views.ClubCreateView.as_view(), name='club-create'),
    path('<int:pk>/', views.ClubDetailView.as_view(), name='club-detail'),
    path('<int:pk>/join/', views.ClubJoinView.as_view(), name='club-join'),
    path('<int:pk>/leave/', views.ClubLeaveView.as_view(), name='club-leave'),
    
    # Club Posts
    path('<int:pk>/posts/', views.ClubPostListView.as_view(), name='club-post-list'),
    path('<int:pk>/posts/create/', views.ClubPostCreateView.as_view(), name='club-post-create'),
    
    # Club Events
    path('<int:pk>/events/', views.ClubEventListView.as_view(), name='club-event-list'),
    path('<int:pk>/events/create/', views.ClubEventCreateView.as_view(), name='club-event-create'),
    path('events/<int:pk>/', views.ClubEventDetailView.as_view(), name='club-event-detail'),
    path('events/<int:pk>/register/', views.EventRegistrationView.as_view(), name='event-register'),
    
    # Club Discussions
    path('<int:pk>/discussions/', views.ClubDiscussionListView.as_view(), name='club-discussion-list'),
    path('<int:pk>/discussions/create/', views.ClubDiscussionCreateView.as_view(), name='club-discussion-create'),
    path('discussions/<int:pk>/', views.ClubDiscussionDetailView.as_view(), name='club-discussion-detail'),
    
    # Club Resources
    path('<int:pk>/resources/', views.ClubResourceListView.as_view(), name='club-resource-list'),
    path('<int:pk>/resources/upload/', views.ClubResourceUploadView.as_view(), name='club-resource-upload'),
]
