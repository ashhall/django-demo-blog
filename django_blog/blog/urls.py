from django.urls import path
from .views import (
	PostListView, 
	PostDetailView, 
	PostCreateView, 
	PostUpdateView, 
	PostDeleteView, 
	UserPostListView,
	UserDraftListView
)
from . import views

urlpatterns = [
    #path('', views.home, name='blog_home'),
    path('', PostListView.as_view(), name='blog_home'),
    path('user/<str:username>/posts/', UserPostListView.as_view(), name='user_posts'),
    path('user/<str:username>/drafts/', UserDraftListView.as_view(), name='user_drafts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/publish/', views.publish_post, name='post_publish'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/like/', views.like_post, name='post_like'),
    # path('post/<int:pk>/comment/', views.add_post_comment, name='add_post_comment'),
    path('about/', views.about, name='blog_about'),
    path('search/', views.search_blog, name='blog_search'),
]