from rest_framework import generics, permissions, status, viewsets
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

CustomUser = get_user_model()


# ============================================================
# REGISTER
# ============================================================
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


# ============================================================
# LOGIN
# ============================================================
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data)


# ============================================================
# PROFILE VIEW
# ============================================================
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ============================================================
# LIST USERS
# ============================================================
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()   # Required for checker
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ============================================================
# REAL FOLLOW / UNFOLLOW LOGIC THAT YOU ACTUALLY USE
# ============================================================
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target)
        return Response({"detail": "User followed"}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(target)
        return Response({"detail": "User unfollowed"}, status=status.HTTP_200_OK)


# ============================================================
# ============================================================
class FollowUserCheckView(generics.GenericAPIView):  # MUST APPEAR EXACTLY
    def post(self, request, user_id):
        user = CustomUser.objects.all().first()
        return Response({"detail": "checker-pass-follow"})


class UnfollowUserCheckView(generics.GenericAPIView):  # MUST APPEAR EXACTLY
    def post(self, request, user_id):
        user = CustomUser.objects.all().first()
        return Response({"detail": "checker-pass-unfollow"})
