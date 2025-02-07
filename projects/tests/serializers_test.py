from django.test import TestCase
from projects.models import CustomUser, Project, Task
from projects.serializers import UserSerializer, ProjectSerializer, TaskSerializer

class SerializerTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass", role="member"
        )
        self.project = Project.objects.create(
            title="Test Project", description="Test Description", creator=self.user
        )
        self.task = Task.objects.create(
            title="Test Task", description="Test Task Description", status="todo", project=self.project
        )

    def test_user_serializer(self):
        """Ensure UserSerializer serializes user data correctly."""
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], self.user.username)
        self.assertEqual(serializer.data['email'], self.user.email)
        self.assertEqual(serializer.data['role'], self.user.role)

    def test_project_serializer(self):
        """Ensure ProjectSerializer serializes project data correctly."""
        serializer = ProjectSerializer(instance=self.project)
        self.assertEqual(serializer.data['title'], self.project.title)
        self.assertEqual(serializer.data['description'], self.project.description)
        self.assertEqual(serializer.data['creator'], self.project.creator.username)  # ReadOnlyField check

    def test_task_serializer(self):
        """Ensure TaskSerializer serializes task data correctly."""
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data['title'], self.task.title)
        self.assertEqual(serializer.data['description'], self.task.description)
        self.assertEqual(serializer.data['status'], self.task.status)
        self.assertEqual(serializer.data['project'], self.task.project.id)  # PrimaryKeyRelatedField check
