import { useEffect, useState } from 'react'
import { Activity, CheckCircle2, AlertCircle } from 'lucide-react'

interface HealthStatus {
  status: string
  db: string
}

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
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
      } catch {
        setError('Backend unreachable')
      }
    }

    checkHealth()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
          <p className="text-sm text-slate-500">Welcome to your personal well-being reflection overview.</p>
        </div>

        {/* Phase 2 Diagnostic Badge preserved per Section C.9 */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-slate-100 border border-slate-200 text-slate-600">
          <Activity className="w-3.5 h-3.5 text-slate-400" />
          {health ? (
            <span className="flex items-center gap-1.5 text-emerald-700">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              Backend: {health.status} / DB: {health.db}
            </span>
          ) : error ? (
            <span className="flex items-center gap-1.5 text-red-600">
              <AlertCircle className="w-3.5 h-3.5 text-red-500" />
              {error}
            </span>
          ) : (
            <span>Checking system...</span>
          )}
        </div>
      </div>

      <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm text-slate-600">
        <h2 className="text-lg font-semibold text-slate-800 mb-2">Application Shell Initialized</h2>
        <p className="text-sm text-slate-500">
          Milestone 1 routing and shell active. Full placeholder widgets will be populated in Milestone 5.
        </p>
      </div>
    </div>
  )
}
