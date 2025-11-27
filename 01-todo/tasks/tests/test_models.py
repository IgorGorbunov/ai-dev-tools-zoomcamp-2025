from django.test import TestCase
from tasks.models import Task

class TaskModelTests(TestCase):
    def test_create_task_defaults(self):
        t = Task.objects.create(title='Test Task')
        self.assertEqual(str(t), 'Test Task')
        self.assertFalse(t.completed)
        self.assertIsNotNone(t.created_at)

    def test_task_due_date_optional(self):
        t = Task.objects.create(title='With Date', due_date=None)
        self.assertIsNone(t.due_date)
