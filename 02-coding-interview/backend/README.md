# Coding Interview Platform - Backend

FastAPI backend for the online coding interview platform.

## Setup

### Prerequisites
- Python 3.10+
- pip or poetry

### Installation

Using poetry:
```bash
cd backend
poetry install
```

Using pip:
```bash
pip install -r requirements.txt
```

### Running the Server

```bash
poetry run uvicorn app.main:app --reload --port 8000
```

or with pip:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Run Tests
```bash
poetry run pytest tests/
```

With coverage:
```bash
poetry run pytest tests/ --cov=app
```

### Verify API

```bash
poetry run python verify_api.py
```

Make sure the server is running before running the verification script.

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── schemas.py           # Pydantic models
│   ├── security.py          # Authentication & security
│   ├── database.py          # Mock database
│   ├── executor.py          # Code execution engine
│   └── routes/
│       ├── auth.py          # Authentication endpoints
│       ├── sessions.py      # Session endpoints
│       └── health.py        # Health check endpoint
├── tests/
│   └── test_api.py          # API tests
├── verify_api.py            # API verification script
├── pyproject.toml           # Poetry dependencies
└── README.md
```

## Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Sessions
- `POST /api/sessions` - Create session
- `GET /api/sessions` - Get user sessions
- `GET /api/sessions/{session_id}` - Get session details
- `PUT /api/sessions/{session_id}` - Update session
- `DELETE /api/sessions/{session_id}` - Delete session
- `POST /api/sessions/{session_id}/execute` - Execute code
- `GET /api/sessions/{session_id}/participants` - Get participants

### Health
- `GET /api/health` - Health check

## Features

- User authentication with JWT
- Create and manage interview sessions
- Real-time code execution
- Support for Python and JavaScript
- Mock database (easily replaceable with real database)
- Comprehensive error handling
- API documentation with OpenAPI/Swagger

## Next Steps

- Replace mock database with PostgreSQL
- Add WebSocket support for real-time collaboration
- Implement user presence tracking
- Add more language support for code execution
