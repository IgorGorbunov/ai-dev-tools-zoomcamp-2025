import api from '@/lib/api'

export interface LoginRequest {
  email: string
  password: string
}

export interface SignupRequest {
  username: string
  email: string
  password: string
}

export interface AuthResponse {
  user: {
    id: string
    username: string
    email: string
    created_at: string
  }
  access_token: string
  token_type: string
}

export const authService = {
  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await api.post('/api/auth/signup', data)
    return response.data
  },

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await api.post('/api/auth/login', data)
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/me')
    return response.data
  },
}

export interface SessionCreateRequest {
  title: string
  language: string
  description?: string
}

export interface Session {
  id: string
  title: string
  language: string
  created_by: string
  created_at: string
  updated_at: string
  participant_count: number
}

export interface SessionDetail extends Session {
  code: string
  description: string
  participants: any[]
}

export const sessionService = {
  async createSession(data: SessionCreateRequest): Promise<Session> {
    const response = await api.post('/api/sessions', data)
    return response.data
  },

  async getSessions(limit = 50, offset = 0) {
    const response = await api.get('/api/sessions', {
      params: { limit, offset }
    })
    return response.data
  },

  async getSessionDetail(sessionId: string): Promise<SessionDetail> {
    const response = await api.get(`/api/sessions/${sessionId}`)
    return response.data
  },

  async updateSession(sessionId: string, data: Partial<SessionCreateRequest>) {
    const response = await api.put(`/api/sessions/${sessionId}`, data)
    return response.data
  },

  async deleteSession(sessionId: string) {
    await api.delete(`/api/sessions/${sessionId}`)
  },

  async executeCode(sessionId: string, code: string, language: string, input?: string) {
    const response = await api.post(`/api/sessions/${sessionId}/execute`, {
      code,
      language,
      input,
    })
    return response.data
  },

  async getParticipants(sessionId: string) {
    const response = await api.get(`/api/sessions/${sessionId}/participants`)
    return response.data
  },
}
