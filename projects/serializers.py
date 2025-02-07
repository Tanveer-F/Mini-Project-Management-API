from rest_framework import serializers
from .models import CustomUser, Project, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Ensure password is properly hashed before saving
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)  # Hash the password
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')  # Display creator's username instead of ID

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'creator']

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # Ensure valid project selection

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project']
