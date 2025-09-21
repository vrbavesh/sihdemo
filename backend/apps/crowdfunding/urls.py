from django.urls import path
from . import views

urlpatterns = [
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/like/', views.ProjectLikeView.as_view(), name='project-like'),
    path('projects/<int:pk>/share/', views.ProjectShareView.as_view(), name='project-share'),
    
    # Contributions
    path('projects/<int:pk>/contribute/', views.ContributionCreateView.as_view(), name='contribute'),
    path('contributions/', views.ContributionListView.as_view(), name='contribution-list'),
    
    # Project Updates
    path('projects/<int:pk>/updates/', views.ProjectUpdateListView.as_view(), name='project-updates'),
    path('projects/<int:pk>/updates/create/', views.ProjectUpdateCreateView.as_view(), name='project-update-create'),
    
    # Refunds
    path('refunds/', views.RefundListView.as_view(), name='refund-list'),
    path('refunds/<int:pk>/', views.RefundDetailView.as_view(), name='refund-detail'),
    
    # Analytics
    path('stats/', views.CrowdfundingStatsView.as_view(), name='crowdfunding-stats'),
]
