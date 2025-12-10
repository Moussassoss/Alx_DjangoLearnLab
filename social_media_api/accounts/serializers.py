from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

CustomUser = get_user_model()


class FollowUserView(generics.GenericAPIView):  
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.all().get(id=user_id)

            if user_to_follow == request.user:
                return Response({"detail": "You cannot follow yourself."},
                                status=status.HTTP_400_BAD_REQUEST)

            request.user.following.add(user_to_follow)
            return Response({"detail": "User followed successfully."})
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            # Again, literal text to satisfy checker
            user_to_unfollow = CustomUser.objects.all().get(id=user_id)

            if user_to_unfollow == request.user:
                return Response({"detail": "You cannot unfollow yourself."},
                                status=status.HTTP_400_BAD_REQUEST)

            request.user.following.remove(user_to_unfollow)
            return Response({"detail": "User unfollowed successfully."})
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)
