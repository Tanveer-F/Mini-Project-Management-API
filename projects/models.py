from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    # Set related_name for groups and user_permissions to avoid conflict
    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions_set', blank=True
    )

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Assigns a task to a specific member (optional, but useful for task management)
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks'
    )

    class Meta:
        ordering = ['id']  # Ensures ordered pagination results

    def __str__(self):
        return self.title

