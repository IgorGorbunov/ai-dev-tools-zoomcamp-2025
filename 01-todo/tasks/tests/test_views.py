from django.test import TestCase
from django.urls import reverse
from tasks.models import Task

class TaskViewsTests(TestCase):
    def test_list_view_shows_tasks(self):
        Task.objects.create(title='A')
        resp = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tasks/task_list.html')
        self.assertContains(resp, 'A')

    def test_create_view_creates_task(self):
        resp = self.client.post(reverse('tasks:task_create'), {
            'title': 'New',
            'description': 'Desc',
            'due_date': '',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New').exists())

    def test_toggle_complete(self):
        t = Task.objects.create(title='Toggle me')
        self.assertFalse(t.completed)
        resp = self.client.post(reverse('tasks:task_toggle', args=[t.pk]))
        self.assertEqual(resp.status_code, 302)
        t.refresh_from_db()
        self.assertTrue(t.completed)
