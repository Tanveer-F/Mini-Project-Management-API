from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class URLsTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")

        # Login to get JWT Token
        login_url = reverse('login')
        response = self.client.post(login_url, {"username": "testuser", "password": "testpassword"}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # If JWT Token Authentication
        self.token = response.data.get("access")  # Adjust key based on your JWT response

        # Set Authorization Header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_register_url(self):
        url = reverse('register')
        data = {"username": "newuser", "password": "newpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_url(self):
        url = reverse('login')
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_projects_url(self):
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should be 200 now

    def test_tasks_url(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should be 200 now
