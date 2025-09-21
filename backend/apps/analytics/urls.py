from django.urls import path
from . import views

urlpatterns = [
    # Analytics
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('events/', views.AnalyticsEventListView.as_view(), name='analytics-events'),
    path('user-engagement/', views.UserEngagementView.as_view(), name='user-engagement'),
    path('platform-metrics/', views.PlatformMetricsView.as_view(), name='platform-metrics'),
    
    # Reports
    path('reports/users/', views.UserReportView.as_view(), name='user-report'),
    path('reports/activity/', views.ActivityReportView.as_view(), name='activity-report'),
    path('reports/financial/', views.FinancialReportView.as_view(), name='financial-report'),
]
