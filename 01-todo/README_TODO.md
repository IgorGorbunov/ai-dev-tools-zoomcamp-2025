TODO Django app

Setup (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

App structure:
- `tasks` app: create/edit/delete tasks, add due dates, mark completed.
- Templates live in `templates/tasks`.

Notes:
- Replace `SECRET_KEY` in `todo_project/settings.py` for production.
- This is a minimal starter — I can add pagination, filtering, or tests next.
