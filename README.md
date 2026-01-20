# ai-dev-tools-zoomcamp-2025

Repo for ai-dev-tools-zoomcamp-2025

**Run & Test Commands**

- **Backend (Python / FastAPI)**:

	- Create virtualenv:

		```powershell
		python -m venv .venv
		.\.venv\Scripts\Activate.ps1  # PowerShell
		# OR
		.\.venv\Scripts\activate.bat  # CMD
		```

	- Install dependencies:

		```powershell
		cd 02-coding-interview/backend
		pip install -r requirements.txt
		```

	- Run the server (development):

		```powershell
		cd 02-coding-interview/backend
		uvicorn app.main:app --reload --port 8000
		```

	- Run backend tests:

		```powershell
		cd 02-coding-interview/backend
		pytest -q
		```

- **Frontend (Vite / TypeScript)**:

	- Install dependencies:

		```bash
		cd 02-coding-interview/frontend
		npm install
		```

	- Start dev server:

		```bash
		cd 02-coding-interview/frontend
		npm run dev
		```

	- Build for production:

		```bash
		cd 02-coding-interview/frontend
		npm run build
		```

	- Run frontend tests (unit):

		```bash
		cd 02-coding-interview/frontend
		npm test
		```

- **Full-stack (quick)**: start the backend (port 8000) and frontend dev server; frontend expects the API at `http://localhost:8000` by default.

**Notes**

- Backend dependencies and tests live in [02-coding-interview/backend](02-coding-interview/backend).
- Frontend sources live in [02-coding-interview/frontend](02-coding-interview/frontend).
