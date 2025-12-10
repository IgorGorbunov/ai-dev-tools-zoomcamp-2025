import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { sessionService } from '@/services/api'
import { useAuthStore } from '@/store/auth'

export const Home: React.FC = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const [sessions, setSessions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [title, setTitle] = useState('')
  const [language, setLanguage] = useState('python')

  useEffect(() => {
    loadSessions()
  }, [])

  const loadSessions = async () => {
    try {
      const data = await sessionService.getSessions()
      setSessions(data.items)
    } catch (err) {
      console.error('Failed to load sessions', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateSession = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await sessionService.createSession({ title, language })
      setTitle('')
      setLanguage('python')
      setShowCreateForm(false)
      loadSessions()
    } catch (err) {
      console.error('Failed to create session', err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Coding Interviews</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm">Welcome, {user?.username}!</span>
            <button
              onClick={logout}
              className="bg-red-500 px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-6">
        {/* Create Session */}
        <div className="mb-8">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 font-semibold"
          >
            {showCreateForm ? 'Cancel' : 'Create New Session'}
          </button>

          {showCreateForm && (
            <form onSubmit={handleCreateSession} className="bg-white p-6 rounded-lg shadow mt-4">
              <div className="mb-4">
                <label className="block text-gray-700 font-semibold mb-2">Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  required
                />
              </div>
              <div className="mb-6">
                <label className="block text-gray-700 font-semibold mb-2">Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="java">Java</option>
                  <option value="cpp">C++</option>
                  <option value="go">Go</option>
                </select>
              </div>
              <button
                type="submit"
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
              >
                Create
              </button>
            </form>
          )}
        </div>

        {/* Sessions List */}
        {loading ? (
          <div className="text-center text-gray-600">Loading sessions...</div>
        ) : sessions.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow text-center text-gray-600">
            No sessions yet. Create one to get started!
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="bg-white p-6 rounded-lg shadow hover:shadow-lg cursor-pointer transition"
                onClick={() => navigate(`/session/${session.id}`)}
              >
                <h3 className="text-lg font-bold mb-2">{session.title}</h3>
                <p className="text-gray-600 mb-2">Language: {session.language}</p>
                <p className="text-gray-600 mb-4">
                  Participants: {session.participant_count}
                </p>
                <button className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
                  Join
                </button>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
