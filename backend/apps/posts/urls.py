from django.urls import path
from . import views

urlpatterns = [
    # Posts
    path('', views.PostListView.as_view(), name='post-list'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/comment/', views.PostCommentView.as_view(), name='post-comment'),
    path('<int:pk>/share/', views.PostShareView.as_view(), name='post-share'),
    path('<int:pk>/bookmark/', views.PostBookmarkView.as_view(), name='post-bookmark'),
    
    # Comments
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:pk>/like/', views.CommentLikeView.as_view(), name='comment-like'),
]
