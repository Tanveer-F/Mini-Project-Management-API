from django.test import TestCase
from projects.models import CustomUser, Project, Task

class ModelsTestCase(TestCase):

    def setUp(self):
        """Set up test users and a project for testing."""
        self.admin_user = CustomUser.objects.create_user(
            username="admin", password="admin123", role="admin"
        )
        self.member_user = CustomUser.objects.create_user(
            username="member", password="member123", role="member"
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Project Description",
            creator=self.admin_user
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Task Description",
            project=self.project,
            assigned_to=self.member_user
        )

    def test_custom_user_creation(self):
        """Ensure that a CustomUser can be created with a role."""
        self.assertEqual(self.admin_user.role, "admin")
        self.assertEqual(self.member_user.role, "member")

    def test_project_creation(self):
        """Ensure that a Project can be created."""
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.creator, self.admin_user)

    def test_task_creation(self):
        """Ensure that a Task can be created and assigned to a member."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assigned_to, self.member_user)

    def test_task_default_status(self):
        """Ensure that the default status of a task is 'todo'."""
        self.assertEqual(self.task.status, "todo")
