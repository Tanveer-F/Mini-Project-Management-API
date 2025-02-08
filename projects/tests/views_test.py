from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from projects.models import CustomUser, Project, Task
from rest_framework_simplejwt.tokens import RefreshToken

class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'role': 'admin'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.token = RefreshToken.for_user(self.user).access_token

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'role': 'member'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class ProjectTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'role': 'admin'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.project_data = {
            'title': 'Test Project',
            'description': 'Test Project Description',
            'creator': self.user
        }
        self.project = Project.objects.create(**self.project_data)

    def test_create_project(self):
        url = reverse('project-list')
        data = {
            'title': 'New Project',
            'description': 'New Project Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_projects(self):
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'role': 'admin'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Project Description',
            creator=self.user
        )
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Task Description',
            'status': 'todo',
            'project': self.project
        }
        self.task = Task.objects.create(**self.task_data)

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'status': 'todo',
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_status(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {'status': 'in_progress'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'in_progress')