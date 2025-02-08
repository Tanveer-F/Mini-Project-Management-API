from django.test import TestCase
from django.contrib.admin.sites import site
from projects.admin import ProjectAdmin, TaskAdmin
from projects.models import Project, Task

class AdminSiteTest(TestCase):
    def test_project_admin_registration(self):
        self.assertIn(Project, site._registry)
        self.assertIsInstance(site._registry[Project], ProjectAdmin)

    def test_task_admin_registration(self):
        self.assertIn(Task, site._registry)
        self.assertIsInstance(site._registry[Task], TaskAdmin)

    def test_project_admin_list_display(self):
        project_admin = site._registry[Project]
        self.assertEqual(project_admin.list_display, ['title', 'creator', 'created_at'])

    def test_task_admin_list_display(self):
        task_admin = site._registry[Task]
        self.assertEqual(task_admin.list_display, ['title', 'project', 'assigned_to', 'status', 'created_at'])