import { useEffect, useState } from 'react'
import { Activity, Info } from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Card from '../../components/ui/Card'
import { apiGet } from '../../api/client'

interface WellBeingResponse {
  date: string
  status: 'no_score' | 'insufficient_history' | 'baseline_available'
  score: number
  baseline: number | null
  difference: number | null
  comparison: 'above' | 'near' | 'below' | null
  baseline_sample_size: number
  history: Array<{
    date: string
    score: number
  }>
}

export default function WellBeingAnalysisPage() {
  const today = new Date().toISOString().split('T')[0]

  const [data, setData] = useState<WellBeingResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    apiGet<WellBeingResponse>(`/api/wellbeing/${today}`)
      .then(setData)
      .catch(() => {
        setError('Well-being analysis is not available for today.')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [today])

  if (loading) {
    return (
      <div className="p-6 text-sm text-slate-500">
        Loading well-being analysis...
      </div>
    )
  }

  if (error || !data) {
    return (
      <Card title="Well-Being Analysis">
        <p className="text-sm text-slate-500">
          {error ?? 'No analysis available.'}
        </p>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5">
        <p className="text-sm font-medium text-slate-500">
          Explainable analysis
        </p>

        <h1 className="mt-1 text-2xl font-bold text-slate-800">
          Well-Being Analysis
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          A personal historical reference based on your own well-being data.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <div className="flex items-center gap-6">
            <div className="flex h-32 w-32 shrink-0 items-center justify-center rounded-full border-8 border-slate-100">
              <div className="text-center">
                <p className="text-4xl font-bold text-slate-800">
                  {data.score}
                </p>
                <p className="text-xs text-slate-500">
                  out of 100
                </p>
              </div>
            </div>

            <div>
              <h2 className="text-lg font-semibold text-slate-800">
                Current Well-Being Index
              </h2>

              {data.status === 'baseline_available' && (
                <Badge
                  variant={
                    data.comparison === 'above'
                      ? 'success'
                      : data.comparison === 'below'
                        ? 'warning'
                        : 'default'
                  }
                >
                  {data.difference !== null && data.difference >= 0 ? '+' : ''}
                  {data.difference} vs baseline
                </Badge>
              )}

              {data.status === 'insufficient_history' && (
                <Badge variant="default">
                  Building personal baseline
                </Badge>
              )}

              <div className="mt-4 flex items-start gap-2 rounded-lg bg-slate-50 p-3">
                <Info className="mt-0.5 h-4 w-4 shrink-0 text-slate-500" />
                <p className="text-xs leading-5 text-slate-500">
                  This index is for personal reflection and behavioral
                  analytics. It is not a medical or clinical measurement.
                </p>
              </div>
            </div>
          </div>
        </Card>

        <Card title="Personal Baseline">
          {data.baseline !== null ? (
            <>
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-slate-100 p-2.5">
                  <Activity className="h-5 w-5 text-slate-600" />
                </div>

                <div>
                  <p className="text-3xl font-bold text-slate-800">
                    {data.baseline.toFixed(1)}
                  </p>
                  <p className="text-xs text-slate-500">
                    Based on {data.baseline_sample_size} previous scores
                  </p>
                </div>
              </div>

              <p className="mt-4 text-sm leading-6 text-slate-600">
                Your baseline uses your own recent historical scores.
              </p>
            </>
          ) : (
            <p className="text-sm leading-6 text-slate-500">
              A personal baseline will become available after at least
              3 previous valid well-being scores.
            </p>
          )}
        </Card>
      </div>
    </div>
  )
}
