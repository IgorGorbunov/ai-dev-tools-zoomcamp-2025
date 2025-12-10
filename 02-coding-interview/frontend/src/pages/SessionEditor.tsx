import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import { sessionService } from '@/services/api'

export const SessionEditor: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>()
  const [session, setSession] = useState<any>(null)
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(true)
  const [executing, setExecuting] = useState(false)
  const [input, setInput] = useState('')

  useEffect(() => {
    loadSession()
    // Poll for updates every 2 seconds
    const interval = setInterval(loadSession, 2000)
    return () => clearInterval(interval)
  }, [sessionId])

  const loadSession = async () => {
    if (!sessionId) return
    try {
      const data = await sessionService.getSessionDetail(sessionId)
      setSession(data)
      setCode(data.code || '')
    } catch (err) {
      console.error('Failed to load session', err)
    } finally {
      setLoading(false)
    }
  }

  const handleExecute = async () => {
    if (!sessionId) return
    setExecuting(true)
    try {
      const result = await sessionService.executeCode(sessionId, code, session.language, input)
      setOutput(result.success ? result.output : `Error: ${result.error}`)
    } catch (err: any) {
      setOutput(`Error: ${err.message}`)
    } finally {
      setExecuting(false)
    }
  }

  const handleSave = async () => {
    if (!sessionId) return
    try {
      await sessionService.updateSession(sessionId, { code })
      alert('Code saved!')
    } catch (err) {
      console.error('Failed to save', err)
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      {/* Header */}
      <div className="bg-gray-800 text-white p-4 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <h1 className="text-xl font-bold">{session?.title}</h1>
          <div className="text-sm">
            Language: <span className="font-semibold">{session?.language}</span>
          </div>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Editor */}
        <div className="flex-1 flex flex-col">
          <Editor
            height="100%"
            language={session?.language === 'javascript' ? 'javascript' : 'python'}
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: 'Fira Code, monospace',
            }}
          />
        </div>

        {/* Sidebar */}
        <div className="w-80 bg-gray-800 border-l border-gray-700 flex flex-col text-white">
          {/* Input */}
          <div className="p-4 border-b border-gray-700">
            <h3 className="font-semibold mb-2">Input (stdin)</h3>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="w-full h-24 bg-gray-900 text-white border border-gray-700 rounded p-2 text-sm"
              placeholder="Enter input here..."
            />
          </div>

          {/* Output */}
          <div className="flex-1 p-4 border-b border-gray-700 overflow-auto">
            <h3 className="font-semibold mb-2">Output</h3>
            <div className="bg-gray-900 rounded p-2 text-sm font-mono whitespace-pre-wrap break-words">
              {output || '(No output yet)'}
            </div>
          </div>

          {/* Actions */}
          <div className="p-4 space-y-2">
            <button
              onClick={handleExecute}
              disabled={executing}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-4 py-2 rounded font-semibold"
            >
              {executing ? 'Executing...' : 'Execute'}
            </button>
            <button
              onClick={handleSave}
              className="w-full bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold"
            >
              Save
            </button>
          </div>

          {/* Participants */}
          <div className="p-4 border-t border-gray-700">
            <h3 className="font-semibold mb-2">Participants ({session?.participants?.length || 0})</h3>
            <div className="space-y-1 text-sm">
              {session?.participants?.map((p: any) => (
                <div key={p.user_id} className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  {p.username}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
