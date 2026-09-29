import { useEffect, useState } from 'react'
import { Activity, CheckCircle2, AlertCircle } from 'lucide-react'

interface HealthStatus {
  status: string
  db: string
}

export default function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function checkHealth() {
      try {
        const response = await fetch('/api/health')
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`)
        }
        const data: HealthStatus = await response.json()
        setHealth(data)
      } catch (err) {
        setError('Backend unreachable')
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Activity className="w-6 h-6 text-indigo-600" />
          <h1 className="text-xl font-bold text-slate-800">MindMirror</h1>
        </div>
        <p className="text-sm text-slate-500 mb-6">
          Phase 2 Project Architecture & Foundation Status
        </p>

        <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
            System Connectivity
          </div>
          {loading && (
            <div className="text-sm text-slate-600">Checking system health...</div>
          )}
          {error && (
            <div className="flex items-center gap-2 text-sm text-red-600 font-medium">
              <AlertCircle className="w-4 h-4" />
              <span>{error}</span>
            </div>
          )}
          {health && (
            <div className="flex items-center gap-2 text-sm text-emerald-700 font-medium">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>
                Backend: {health.status} / DB: {health.db}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
