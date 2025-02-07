from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrTaskUpdater
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model

User = get_user_model()

# User Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=201)
        return Response(serializer.errors, status=400)

# User Login with JWT
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({'error': 'Invalid credentials'}, status=401)

# Pagination for Task List
class TaskPagination(PageNumberPagination):
    page_size = 10

# Project ViewSet - Only Admins can create/delete, Users see only their own projects
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:  # Admins can see all projects
            return Project.objects.all()
        return Project.objects.filter(creator=self.request.user)  # Users see only their own projects

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)  # Assign project to authenticated admin

# Task ViewSet - Only Admins can create/delete, Members can update task status
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTaskUpdater]
    pagination_class = TaskPagination

    def get_queryset(self):
        """
        Users see only the tasks from their own projects
        Admins can see all tasks.
        """
        if self.request.user.is_staff:  # Admins see all tasks
            return Task.objects.all()
        return Task.objects.filter(project__creator=self.request.user) 
    def perform_create(self, serializer):
        """
        When creating a task, ensure it's associated with a project.
        """
        project = Project.objects.get(id=self.request.data.get('project'))  
        serializer.save(project=project, assigned_to=self.request.user)  