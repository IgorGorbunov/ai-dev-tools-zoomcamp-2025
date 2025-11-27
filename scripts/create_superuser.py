import os
import sys
import pathlib
import django

# Ensure project root is on sys.path when script executed from scripts/
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@example.com'
password = 'adminpass'

if User.objects.filter(username=username).exists():
    print('Superuser already exists:', username)
else:
    User.objects.create_superuser(username, email, password)
    print('Created superuser:', username)
