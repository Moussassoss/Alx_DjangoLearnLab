# blog/urls.py
from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    add_comment, edit_comment, delete_comment, RegisterView, ProfileView
)
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # comments
    path('posts/<int:post_pk>/comments/add/', add_comment, name='add_comment'),
    path('comments/<int:comment_pk>/edit/', edit_comment, name='edit_comment'),
    path('comments/<int:comment_pk>/delete/', delete_comment, name='delete_comment'),

    # auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:post_list'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
