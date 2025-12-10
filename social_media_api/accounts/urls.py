from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, ProfileView, UserViewSet, FollowUnfollowAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUnfollowAPIView.as_view(), name='follow'),
]
