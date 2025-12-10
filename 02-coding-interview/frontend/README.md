# Frontend Documentation

Complete guide for the React/TypeScript frontend of the Coding Interview Platform.

## Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML entry point
├── src/
│   ├── main.tsx                # Vite entry point
│   ├── App.tsx                 # Main app component with React Router
│   ├── index.css               # Global styles with Tailwind
│   ├── lib/
│   │   └── api.ts              # Axios HTTP client with JWT interceptor
│   ├── store/
│   │   └── auth.ts             # Zustand state management
│   ├── services/
│   │   └── api.ts              # Type-safe API service layer
│   ├── components/
│   │   └── ProtectedRoute.tsx   # Route authentication guard
│   └── pages/
│       ├── Login.tsx            # Login page
│       ├── Signup.tsx           # Signup page
│       ├── Home.tsx             # Dashboard - session list
│       └── SessionEditor.tsx    # Code editor with execution
├── package.json                # NPM configuration
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite build configuration
└── README.md                   # This file
```

## Setup

### Prerequisites
- Node.js 16+ and npm
- Backend running on `http://localhost:8000`

### Installation

```bash
cd frontend

# Install all dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting (if configured)
npm run lint
```

## Architecture

### State Management (Zustand)

**Authentication Store** (`src/store/auth.ts`):
```typescript
useAuthStore({
  user: User | null,           // Current authenticated user
  token: string | null,        // JWT access token
  isAuthenticated: boolean,    // Auth status
  setAuth: (user, token),      // Set after login/signup
  clearAuth: (),               // Clear on logout
  logout: ()                   // Logout with redirect
})
```

**Session Store** (`src/store/auth.ts`):
```typescript
useSessionStore({
  sessions: Session[],         // List of sessions
  currentSession: Session | null,
  setSessions: (sessions),
  setCurrentSession: (session),
  clearCurrentSession: ()
})
```

### API Client (Axios)

**Configuration** (`src/lib/api.ts`):
- Base URL: `http://localhost:8000/api`
- Auto-injects JWT token from localStorage to all requests
- Auto-redirects to login on 401 (Unauthorized)
- Error handling with optional toast notifications

### Service Layer

**API Service** (`src/services/api.ts`) provides typed methods:

```typescript
// Auth
authService.signup(data)
authService.login(email, password)
authService.getCurrentUser()

// Sessions
sessionService.createSession(data)
sessionService.getSessions(params)
sessionService.getSessionDetail(id)
sessionService.updateSession(id, data)
sessionService.deleteSession(id)
sessionService.executeCode(sessionId, code, language, input)
sessionService.getParticipants(sessionId)
```

## Page Components

### Login Page (`src/pages/Login.tsx`)
- Email and password form
- Form validation and error handling
- Loading state during submission
- Link to signup page
- Redirect to home on successful login

**Props:** None (uses auth store)
**State:** email, password, error, loading

### Signup Page (`src/pages/Signup.tsx`)
- Username, email, password form
- Password validation (minimum 8 characters)
- Error handling
- Link to login page
- Redirect to home on successful signup

**Props:** None (uses auth store)
**State:** username, email, password, error, loading

### Home Page / Dashboard (`src/pages/Home.tsx`)
- List all user's sessions
- Create new session form
- Session cards with join button
- Responsive grid layout

**Features:**
- Fetch sessions on mount
- Create session with title and language selection
- Delete session (for creator)
- Navigate to SessionEditor on join

**State:**
- sessions: Session[]
- loading: boolean
- showCreateForm: boolean
- title: string (form)
- language: string (form)

### Session Editor (`src/pages/SessionEditor.tsx`)
- Monaco Editor for code editing
- Code execution panel with input/output
- Participants list
- Save button
- Language selection display

**Features:**
- Fetch session details on mount
- Auto-save code every 2 seconds (polling)
- Execute code with custom input
- Display execution output
- Show live participants

**Dependencies:**
- `@monaco-editor/react` - Code editor component
- `sessionService` - API calls

**State:**
- session: Session | null
- code: string
- output: string
- loading: boolean
- executing: boolean
- input: string

## Routing

**React Router Setup** (`src/App.tsx`):

```
/login          → Login page (public)
/signup         → Signup page (public)
/               → Home/Dashboard (protected)
/session/:id    → SessionEditor (protected)
/*              → Redirect to home
```

**Route Protection:**
- `ProtectedRoute` component checks authentication
- Redirects to `/login` if not authenticated
- Wraps all protected pages

## Styling

### TailwindCSS

All components use Tailwind utility classes for styling:
- Responsive: `md:`, `lg:` breakpoints
- Colors: `bg-blue-500`, `text-gray-700`
- Spacing: `p-4`, `mb-8`, `gap-6`
- Flexbox: `flex`, `items-center`, `justify-between`

### Global Styles (`src/index.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: system fonts;
  -webkit-font-smoothing: antialiased;
}

code {
  font-family: 'Fira Code', monospace;
}
```

## Development Workflow

### Adding a New Page

1. Create page component: `src/pages/NewPage.tsx`
2. Import in `src/App.tsx`
3. Add route in `<Routes>`
4. Implement page logic with hooks

Example:
```typescript
// src/pages/NewPage.tsx
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/auth'

export const NewPage: React.FC = () => {
  const { user } = useAuthStore()
  
  return <div>Hello {user?.username}</div>
}
```

### Adding a New API Endpoint

1. Add TypeScript interface in `src/services/api.ts`
2. Add method to appropriate service (authService, sessionService, etc.)
3. Use in component via `import { sessionService } from '@/services/api'`

Example:
```typescript
// Add to src/services/api.ts
export const newService = {
  getNewData: async () => {
    const response = await api.get('/new-endpoint')
    return response.data
  },
}

// Use in component
const data = await newService.getNewData()
```

### State Management

For shared state across components, add to Zustand store:

```typescript
// src/store/auth.ts
const useNewStore = create((set) => ({
  data: null,
  setData: (data) => set({ data }),
  clearData: () => set({ data: null }),
}))

// Use in components
const { data, setData } = useNewStore()
```

## Environment Variables

Create `.env` file in frontend root:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_BASE_URL
```

## Type Safety

All components and services use TypeScript with strict mode enabled.

### Key Type Definitions

```typescript
// User
interface User {
  id: string
  username: string
  email: string
}

// Session
interface Session {
  id: string
  title: string
  language: string
  code: string
  created_by: string
  created_at: string
  updated_at: string
  participant_count: number
  participants: Participant[]
}

// Execution Result
interface ExecutionResult {
  success: boolean
  output: string
  error?: string
  execution_time: number
}
```

See `src/services/api.ts` for complete type definitions.

## Common Tasks

### Display Loading State
```typescript
const [loading, setLoading] = useState(true)

if (loading) return <div>Loading...</div>
```

### Handle API Errors
```typescript
try {
  const data = await sessionService.getSessions()
} catch (err: any) {
  setError(err.response?.data?.message || 'An error occurred')
}
```

### Access Current User
```typescript
const { user, isAuthenticated } = useAuthStore()

if (!isAuthenticated) return <Navigate to="/login" />
```

### Make Authenticated API Call
```typescript
// Token automatically added by Axios interceptor
const response = await api.get('/protected-endpoint')
```

### Navigate Programmatically
```typescript
const navigate = useNavigate()
navigate('/dashboard')
```

## Performance Optimization

### Code Splitting
Routes are automatically code-split by Vite

### Memoization
Use `React.memo()` for expensive components

### State Optimization
Keep state as local as possible; only use Zustand for truly shared state

### Image Optimization
Use WebP format when possible
Lazy load images with `loading="lazy"`

## Debugging

### Browser DevTools
1. Open DevTools (F12)
2. React tab: Inspect component tree and props
3. Redux/Store tab: Inspect state changes
4. Network tab: Monitor API calls
5. Console: View errors and logs

### Logging
```typescript
console.log('Debug:', data)
console.error('Error:', error)
console.warn('Warning:', warning)
```

### API Debugging
All API requests go through Axios. Add logging in `src/lib/api.ts`:
```typescript
api.interceptors.request.use((config) => {
  console.log('Request:', config)
  return config
})
```

## Testing

### Setup
```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

### Example Test
```typescript
// src/__tests__/Login.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Login } from '../pages/Login'

describe('Login Page', () => {
  it('renders email input', () => {
    render(<Login />)
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
  })
})
```

### Run Tests
```bash
npm test
npm test -- --coverage
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android 90+)

## Troubleshooting

### "Cannot find module" errors
- Run `npm install`
- Restart dev server: `npm run dev`
- Clear cache: `rm -rf node_modules && npm install`

### Styling not working
- Check TailwindCSS setup in `vite.config.ts`
- Verify `src/index.css` has Tailwind imports
- Clear browser cache

### API requests failing
- Check backend is running on `http://localhost:8000`
- Verify CORS settings in backend
- Check network tab in DevTools

### TypeScript errors
- Run `npm run type-check`
- Update tsconfig.json if needed
- Restart dev server

## Best Practices

1. **Type Everything**: Use TypeScript interfaces for all data
2. **Handle Errors**: Always wrap API calls in try-catch
3. **Loading States**: Show loading indicator during data fetch
4. **Error Messages**: Display user-friendly error messages
5. **Responsive Design**: Test on mobile devices
6. **Accessibility**: Use semantic HTML and ARIA labels
7. **Performance**: Lazy load large components
8. **Security**: Never expose secrets in client code

## Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Axios Documentation](https://axios-http.com)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Monaco Editor React](https://github.com/smonaco-editor/react)

## Contributing

Please follow the existing code style and conventions when contributing.
