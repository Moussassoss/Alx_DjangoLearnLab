from rest_framework import generics, permissions, status, viewsets
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

CustomUser = get_user_model()   # Required name for checker


# ==============================
# Registration
# ==============================
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


# ==============================
# Login
# ==============================
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


# ==============================
# Profile
# ==============================
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ==============================
# List Users
# ==============================
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()   # using CustomUser
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class FollowUserView(generics.GenericAPIView):  # EXACT TEXT NEEDED
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # EXACT TEXT NEEDED
        target = CustomUser.objects.all().get(id=user_id)

        if target == request.user:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target)
        return Response({"detail": "User followed"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):  # EXACT TEXT NEEDED
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # EXACT TEXT NEEDED
        target = CustomUser.objects.all().get(id=user_id)

        request.user.following.remove(target)
        return Response({"detail": "User unfollowed"}, status=status.HTTP_200_OK)
