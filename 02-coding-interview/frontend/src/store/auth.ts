import { create } from 'zustand'

interface User {
  id: string
  username: string
  email: string
  created_at: string
}

interface AuthStore {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  setAuth: (user: User, token: string) => void
  clearAuth: () => void
  logout: () => void
}

export const useAuthStore = create<AuthStore>((set) => {
  // Restore from localStorage on init
  const savedToken = localStorage.getItem('access_token')
  const savedUser = localStorage.getItem('user')

  return {
    user: savedUser ? JSON.parse(savedUser) : null,
    token: savedToken,
    isAuthenticated: !!savedToken,
    
    setAuth: (user, token) => {
      localStorage.setItem('access_token', token)
      localStorage.setItem('user', JSON.stringify(user))
      set({
        user,
        token,
        isAuthenticated: true,
      })
    },

    clearAuth: () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      set({
        user: null,
        token: null,
        isAuthenticated: false,
      })
    },

    logout: () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      set({
        user: null,
        token: null,
        isAuthenticated: false,
      })
    },
  }
})

interface SessionStore {
  sessions: any[]
  currentSession: any | null
  setSessions: (sessions: any[]) => void
  setCurrentSession: (session: any) => void
  clearCurrentSession: () => void
}

export const useSessionStore = create<SessionStore>((set) => ({
  sessions: [],
  currentSession: null,
  setSessions: (sessions) => set({ sessions }),
  setCurrentSession: (session) => set({ currentSession: session }),
  clearCurrentSession: () => set({ currentSession: null }),
}))
