# Online Coding Interview Platform

A professional-grade web application for conducting real-time coding interviews with live code editing, execution, and collaboration features.

## Architecture Overview

```
02-coding-interview/
├── openapi/
│   └── openapi.yaml          # Complete API specification (OpenAPI 3.0)
├── backend/                   # FastAPI backend (Python)
│   ├── app/
│   │   ├── main.py           # FastAPI application setup
│   │   ├── config.py         # Configuration & settings
│   │   ├── schemas.py        # Pydantic models
│   │   ├── security.py       # JWT & password utilities
│   │   ├── database.py       # Mock database
│   │   ├── executor.py       # Code execution engine
│   │   └── routes/
│   │       ├── auth.py       # Authentication endpoints
│   │       ├── sessions.py   # Session management endpoints
│   │       └── health.py     # Health check
│   ├── tests/
│   │   └── test_api.py       # Comprehensive test suite
│   ├── requirements.txt       # Python dependencies
│   ├── pyproject.toml        # Poetry configuration
│   └── README.md             # Backend documentation
└── frontend/                  # React frontend (TypeScript)
    ├── src/
    │   ├── main.tsx          # Vite entry point
    │   ├── App.tsx           # Main app component with routing
    │   ├── index.css         # Global styles & Tailwind
    │   ├── lib/
    │   │   └── api.ts        # Axios HTTP client with interceptors
    │   ├── store/
    │   │   └── auth.ts       # Zustand state management
    │   ├── services/
    │   │   └── api.ts        # Type-safe API service layer
    │   ├── components/
    │   │   └── ProtectedRoute.tsx  # Authentication guard
    │   └── pages/
    │       ├── Login.tsx      # Login page
    │       ├── Signup.tsx     # Signup page
    │       ├── Home.tsx       # Dashboard (session list)
    │       └── SessionEditor.tsx    # Code editor & execution
    ├── index.html            # HTML entry point
    ├── package.json          # NPM dependencies
    ├── tsconfig.json         # TypeScript configuration
    ├── vite.config.ts        # Vite build configuration
    └── README.md             # Frontend documentation
```

## Technology Stack

### Backend
- **FastAPI** 0.104.0+ - Async REST API framework
- **Python** 3.10+ - Runtime
- **Pydantic** 2.0+ - Data validation
- **JWT** (python-jose) - Token authentication
- **pytest** - Testing framework

### Frontend
- **React** 18.2.0 - UI library
- **TypeScript** 5.3+ - Type-safe JavaScript
- **Vite** 5.0.0 - Build tool
- **Zustand** 4.4.0 - State management
- **Axios** 1.6.0 - HTTP client
- **react-router-dom** 6.17.0 - Routing
- **Monaco Editor** - Code editor
- **TailwindCSS** 3.3.0 - Styling

## Features

### Authentication
- User registration with email validation
- Secure login with JWT tokens
- Protected routes and endpoints
- Automatic token injection in API requests
- Logout functionality

### Interview Sessions
- Create coding interview sessions
- Select programming language (Python, JavaScript, Java, C++, Go)
- Join existing sessions as participant
- Real-time code sharing and editing
- Session details and participant tracking

### Code Execution
- Execute code directly in browser
- Support for Python and JavaScript
- Configurable input/stdin
- Capture and display output/stdout
- Error handling and timeouts
- Execution time tracking

### User Interface
- Clean, modern dashboard
- Session creation and management
- Full-featured code editor with syntax highlighting
- Real-time output display
- Responsive design for desktop and tablet

## Getting Started

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using database)
# alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`
- API: `http://localhost:8000/api`
- Docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Full Stack Development

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_api.py::test_login
```

### API Verification

```bash
cd backend

# Make sure backend is running (uvicorn app.main:app --reload)
# In another terminal:
python verify_api.py
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Sessions
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List user's sessions
- `GET /api/sessions/{id}` - Get session details
- `PUT /api/sessions/{id}` - Update session
- `DELETE /api/sessions/{id}` - Delete session

### Code Execution
- `POST /api/sessions/{id}/execute` - Execute code

### Participants
- `GET /api/sessions/{id}/participants` - List session participants

### Health
- `GET /api/health` - Server health check

See `openapi/openapi.yaml` for complete API specification.

## Environment Variables

### Backend (`.env`)
```
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:5173
DEBUG=True
```

### Frontend (`.env`)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Project Structure

### Authentication Flow
1. User signs up at `/signup` → Email validation → Account creation
2. User logs in at `/login` → Credentials verified → JWT token generated
3. Token stored in localStorage
4. Axios interceptor adds token to all requests
5. Protected routes redirect to login if no valid token

### Session Flow
1. Authenticated user creates session on Dashboard
2. Session gets unique ID and share URL
3. Other users can join via share URL
4. Code changes synced across participants (polling-based currently)
5. Code execution available to all participants

### Code Execution Flow
1. User enters code in Monaco Editor
2. Selects language and enters input
3. Clicks "Execute" button
4. Code sent to `/api/sessions/{id}/execute`
5. Backend executes in subprocess with timeout
6. Output displayed in output panel

## Future Enhancements

### Real-Time Collaboration
- [ ] WebSocket integration (Socket.io)
- [ ] Real-time code synchronization
- [ ] Live cursor positions for participants
- [ ] Chat for interviewer/interviewee communication

### Code Execution
- [ ] Extend language support (Java, C++, Go, C#, Rust)
- [ ] Docker-based execution for safety
- [ ] Memory and CPU limits
- [ ] Custom test case validation

### User Features
- [ ] User profiles and statistics
- [ ] Interview history and notes
- [ ] Code templates for different problems
- [ ] Problem difficulty levels
- [ ] Time tracking per session

### Infrastructure
- [ ] PostgreSQL database integration
- [ ] User authentication (OAuth2, Google, GitHub)
- [ ] Session recording and playback
- [ ] Email notifications
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Production deployment (AWS, GCP, Azure)

## Development Workflow

1. **Feature Development:**
   - Create feature branch: `git checkout -b feature/my-feature`
   - Implement feature in frontend and/or backend
   - Write tests
   - Create pull request

2. **Backend Development:**
   - Update schemas if models change
   - Update routes
   - Add tests in `tests/test_api.py`
   - Run `pytest` to validate
   - Run `python verify_api.py` to test all endpoints

3. **Frontend Development:**
   - Use TypeScript for type safety
   - Update API service in `src/services/api.ts` if endpoints change
   - Update state management in `src/store/`
   - Create/update components and pages
   - Use TailwindCSS for styling

## Troubleshooting

### "Cannot connect to backend"
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend/app/config.py`
- Verify Vite proxy in `frontend/vite.config.ts`

### "JWT token expired"
- Tokens expire after 24 hours by default
- User will be redirected to login automatically
- Adjust `JWT_EXPIRATION_HOURS` in backend config

### "Code execution timeout"
- Default timeout is 5 seconds
- Increase `TIMEOUT` in `backend/app/executor.py` if needed
- Check for infinite loops in submitted code

### Module import errors in frontend
- Run `npm install` to ensure all dependencies installed
- Clear `.node_modules` and `npm install` again if issues persist
- Check that `vite.config.ts` has proper proxy configuration

## Contributing

Please follow these guidelines:
- Use TypeScript/Python with proper type hints
- Write tests for new features
- Follow existing code style
- Update documentation when adding features
- Use conventional commit messages

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- Check existing GitHub issues
- Create new issue with detailed description
- Join our community Discord (if available)
- Email: support@codinginterviews.dev
