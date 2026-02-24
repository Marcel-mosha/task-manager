from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'user_id', 'title', 'description', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']
    
    def create(self, validated_data):
        """Create a task with the current user"""
        # Remove user_id if present, we'll use request.user
        validated_data.pop('user_id', None)
        # Get user from context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class TaskListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing tasks"""
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']
