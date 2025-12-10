# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ['id','actor','verb','target_content_type','target_object_id','unread','timestamp']
