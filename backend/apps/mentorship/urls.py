from django.urls import path
from . import views

urlpatterns = [
    # Programs
    path('programs/', views.MentorshipProgramListView.as_view(), name='program-list'),
    path('programs/<int:pk>/', views.MentorshipProgramDetailView.as_view(), name='program-detail'),
    
    # Mentor Profiles
    path('mentors/', views.MentorProfileListView.as_view(), name='mentor-list'),
    path('mentors/<int:pk>/', views.MentorProfileDetailView.as_view(), name='mentor-detail'),
    path('mentors/profile/', views.MentorProfileView.as_view(), name='mentor-profile'),
    
    # Requests
    path('requests/', views.MentorshipRequestListView.as_view(), name='request-list'),
    path('requests/create/', views.MentorshipRequestCreateView.as_view(), name='request-create'),
    path('requests/<int:pk>/', views.MentorshipRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:pk>/respond/', views.MentorshipRequestResponseView.as_view(), name='request-response'),
    
    # Sessions
    path('sessions/', views.MentorshipSessionListView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', views.MentorshipSessionDetailView.as_view(), name='session-detail'),
    path('sessions/<int:pk>/start/', views.SessionStartView.as_view(), name='session-start'),
    path('sessions/<int:pk>/end/', views.SessionEndView.as_view(), name='session-end'),
    
    # Feedback
    path('feedback/', views.MentorshipFeedbackListView.as_view(), name='feedback-list'),
    path('feedback/create/', views.MentorshipFeedbackCreateView.as_view(), name='feedback-create'),
    
    # Goals
    path('goals/', views.MentorshipGoalListView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', views.MentorshipGoalDetailView.as_view(), name='goal-detail'),
]
