import { useEffect, useMemo, useState } from 'react'
import {
  BarChart3,
  CalendarDays,
} from 'lucide-react'

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import Card from '../../components/ui/Card'
import ChartContainer from '../../components/ui/ChartContainer'
import { apiGet } from '../../api/client'

type Granularity = 'daily' | 'weekly' | 'monthly'

interface AnalyticsMeta {
  start_date: string
  end_date: string
  granularity: Granularity
}

interface WellBeingPoint {
  date?: string
  period?: string
  period_start?: string
  period_end?: string
  score: number | null
  baseline: number | null
  difference: number | null
  comparison: 'above' | 'near' | 'below' | null
  baseline_status?: string
  average?: number | null
  minimum?: number | null
  maximum?: number | null
  sample_size: number
  is_partial_period?: boolean
}

interface HabitPoint {
  date?: string
  period?: string
  period_start?: string
  period_end?: string
  completed_habits: number
  applicable_habits: number
  completion_rate: number | null
  is_partial_period?: boolean
}

interface NLPPoint {
  date?: string
  period?: string
  period_start?: string
  period_end?: string
  sentiment: number | null
  positive_emotion: number | null
  negative_emotion: number | null
  stress: number | null
  sample_size: number
  is_partial_period?: boolean
}

interface WellBeingResponse {
  meta: AnalyticsMeta
  summary: {
    count: number
    first_scored_date: string | null
    last_scored_date: string | null
    latest_baseline: number | null
    average: number | null
    minimum: number | null
    maximum: number | null
    sample_size: number
  }
  data: WellBeingPoint[]
}

interface HabitResponse {
  meta: AnalyticsMeta
  data: HabitPoint[]
  habit_performance: Array<{
    habit_id: number
    name: string
    days_applicable: number
    days_completed: number
    completion_rate: number | null
  }>
}

interface NLPResponse {
  meta: AnalyticsMeta
  data: NLPPoint[]
}

function getDefaultStartDate(): string {
  const today = new Date()
  const start = new Date(today)
  start.setDate(today.getDate() - 29)

  return start.toISOString().split('T')[0]
}

function getToday(): string {
  return new Date().toISOString().split('T')[0]
}

function formatLabel(value: string | undefined): string {
  if (!value) {
    return ''
  }

  if (value.includes('-W')) {
    return value
  }

  if (/^\d{4}-\d{2}$/.test(value)) {
    const [year, month] = value.split('-').map(Number)

    return new Date(year, month - 1, 1).toLocaleDateString(
      'en-IN',
      {
        month: 'short',
        year: 'numeric',
      },
    )
  }

  return new Date(`${value}T00:00:00`).toLocaleDateString(
    'en-IN',
    {
      day: 'numeric',
      month: 'short',
    },
  )
}

export default function AnalyticsHistoryPage() {
  const [startDate, setStartDate] = useState(getDefaultStartDate)
  const [endDate, setEndDate] = useState(getToday)
  const [granularity, setGranularity] =
    useState<Granularity>('daily')

  const [wellbeing, setWellbeing] =
    useState<WellBeingResponse | null>(null)

  const [habits, setHabits] =
    useState<HabitResponse | null>(null)

  const [nlp, setNlp] =
    useState<NLPResponse | null>(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    if (startDate > endDate) {
      setError('Start date must be before or equal to end date.')
      setLoading(false)
      return
    }

    setLoading(true)
    setError(null)

    const query = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      granularity,
    })

    Promise.all([
      apiGet<WellBeingResponse>(
        `/api/analytics/wellbeing?${query.toString()}`,
      ),
      apiGet<HabitResponse>(
        `/api/analytics/habits?${query.toString()}`,
      ),
      apiGet<NLPResponse>(
        `/api/analytics/nlp?${query.toString()}`,
      ),
    ])
      .then(([wellbeingData, habitData, nlpData]) => {
        if (!active) {
          return
        }

        setWellbeing(wellbeingData)
        setHabits(habitData)
        setNlp(nlpData)
      })
      .catch(() => {
        if (!active) {
          return
        }

        setError(
          'Analytics could not be loaded. Please try again.',
        )
      })
      .finally(() => {
        if (active) {
          setLoading(false)
        }
      })

    return () => {
      active = false
    }
  }, [startDate, endDate, granularity])

  const wellbeingChartData = useMemo(() => {
    return (
      wellbeing?.data.map((point) => ({
        label: formatLabel(point.date ?? point.period),
        score:
          point.score ??
          point.average ??
          null,
        baseline:
          granularity === 'daily'
            ? point.baseline
            : wellbeing.summary.latest_baseline,
      })) ?? []
    )
  }, [wellbeing, granularity])

  const habitChartData = useMemo(() => {
    return (
      habits?.data.map((point) => ({
        label: formatLabel(point.date ?? point.period),
        completionRate: point.completion_rate,
      })) ?? []
    )
  }, [habits])

  const nlpChartData = useMemo(() => {
    return (
      nlp?.data.map((point) => ({
        label: formatLabel(point.date ?? point.period),
        sentiment: point.sentiment,
        stress: point.stress,
      })) ?? []
    )
  }, [nlp])

  const hasAnyData =
    wellbeingChartData.some(
      (point) => point.score !== null,
    ) ||
    habitChartData.some(
      (point) => point.completionRate !== null,
    ) ||
    nlpChartData.some(
      (point) =>
        point.sentiment !== null ||
        point.stress !== null,
    )

  if (loading) {
    return (
      <div className="p-6 text-sm text-slate-500">
        Loading analytics...
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 border-b border-slate-200 pb-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Personal history
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-800">
            Analytics & History
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Explore patterns in your historical well-being,
            habits, and journal signals.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <CalendarDays className="h-4 w-4 text-slate-400" />

          <input
            type="date"
            value={startDate}
            onChange={(event) =>
              setStartDate(event.target.value)
            }
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700"
            aria-label="Analytics start date"
          />

          <span className="text-sm text-slate-400">
            to
          </span>

          <input
            type="date"
            value={endDate}
            onChange={(event) =>
              setEndDate(event.target.value)
            }
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700"
            aria-label="Analytics end date"
          />

          <select
            value={granularity}
            onChange={(event) =>
              setGranularity(
                event.target.value as Granularity,
              )
            }
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700"
            aria-label="Select analytics granularity"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
      </div>

      {error && (
        <Card>
          <p className="text-sm text-red-600">
            {error}
          </p>
        </Card>
      )}

      {!error && !hasAnyData && (
        <Card title="No analytics available">
          <p className="text-sm leading-6 text-slate-500">
            There is not enough historical data in the
            selected period to display analytics yet.
          </p>
        </Card>
      )}

      {!error && hasAnyData && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <Card>
              <p className="text-sm text-slate-500">
                Average Index
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {wellbeing?.summary.average !== null &&
                wellbeing?.summary.average !== undefined
                  ? wellbeing.summary.average.toFixed(1)
                  : '—'}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                {wellbeing?.summary.sample_size ?? 0}{' '}
                scored days
              </p>
            </Card>

            <Card>
              <p className="text-sm text-slate-500">
                Latest Baseline
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {wellbeing?.summary.latest_baseline !==
                  null &&
                wellbeing?.summary.latest_baseline !==
                  undefined
                  ? wellbeing.summary.latest_baseline.toFixed(
                      1,
                    )
                  : '—'}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Personal historical reference
              </p>
            </Card>

            <Card>
              <p className="text-sm text-slate-500">
                Habit Completion
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {(() => {
                  const values =
                    habits?.data
                      .map(
                        (point) =>
                          point.completion_rate,
                      )
                      .filter(
                        (
                          value,
                        ): value is number =>
                          value !== null,
                      ) ?? []

                  if (!values.length) {
                    return '—'
                  }

                  const average =
                    values.reduce(
                      (sum, value) =>
                        sum + value,
                      0,
                    ) / values.length

                  return `${Math.round(
                    average * 100,
                  )}%`
                })()}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Selected period
              </p>
            </Card>

            <Card>
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-slate-500">
                    Scored Days
                  </p>

                  <p className="mt-2 text-3xl font-bold text-slate-800">
                    {wellbeing?.summary.count ?? 0}
                  </p>

                  <div className="mt-2 flex items-center gap-1 text-xs text-slate-500">
                    <BarChart3 className="h-3.5 w-3.5" />
                    Historical observations
                  </div>
                </div>
              </div>
            </Card>
          </div>

          <ChartContainer
            title="Well-Being Index Trend"
            description="Well-being scores compared with your personal baseline."
          >
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={wellbeingChartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="label"
                  tick={{ fontSize: 12 }}
                />

                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 12 }}
                />

                <Tooltip />
                <Legend />

                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#334155"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                  connectNulls={false}
                  name="Well-Being Index"
                />

                <Line
                  type="monotone"
                  dataKey="baseline"
                  stroke="#94a3b8"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  connectNulls={false}
                  name="Personal Baseline"
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>

          <ChartContainer
            title="Habit Consistency"
            description="Habit completion across the selected period."
          >
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={habitChartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="label"
                  tick={{ fontSize: 12 }}
                />

                <YAxis
                  domain={[0, 1]}
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) =>
                    `${Math.round(value * 100)}%`
                  }
                />

                <Tooltip
                  formatter={(value) =>
                    value === null
                      ? 'Unavailable'
                      : `${Math.round(
                          Number(value) * 100,
                        )}%`
                  }
                />

                <Line
                  type="monotone"
                  dataKey="completionRate"
                  stroke="#475569"
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                  connectNulls={false}
                  name="Habit Completion"
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>

          <ChartContainer
            title="NLP Signal Trends"
            description="Sentiment and stress-related signals extracted from journal entries."
          >
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={nlpChartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="label"
                  tick={{ fontSize: 12 }}
                />

                <YAxis
                  domain={[0, 1]}
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) =>
                    `${Math.round(value * 100)}%`
                  }
                />

                <Tooltip
                  formatter={(value) =>
                    value === null
                      ? 'Unavailable'
                      : `${Math.round(
                          Number(value) * 100,
                        )}%`
                  }
                />

                <Legend />

                <Line
                  type="monotone"
                  dataKey="sentiment"
                  stroke="#334155"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                  connectNulls={false}
                  name="Sentiment"
                />

                <Line
                  type="monotone"
                  dataKey="stress"
                  stroke="#94a3b8"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                  connectNulls={false}
                  name="Stress Signal"
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>

          <Card
            title="How to read these trends"
            description="These analytics describe patterns in your own historical data."
          >
            <div className="grid gap-4 text-sm text-slate-600 md:grid-cols-3">
              <div className="rounded-lg bg-slate-50 p-4">
                <p className="font-semibold text-slate-800">
                  Personal baseline
                </p>
                <p className="mt-1 leading-5">
                  Your baseline provides a historical
                  reference based on your own data.
                </p>
              </div>

              <div className="rounded-lg bg-slate-50 p-4">
                <p className="font-semibold text-slate-800">
                  Journal signals
                </p>
                <p className="mt-1 leading-5">
                  Sentiment and stress-related values are
                  extracted text signals, not diagnoses.
                </p>
              </div>

              <div className="rounded-lg bg-slate-50 p-4">
                <p className="font-semibold text-slate-800">
                  Historical patterns
                </p>
                <p className="mt-1 leading-5">
                  Analytics describe patterns and should not
                  be interpreted as proof of cause and effect.
                </p>
              </div>
            </div>

            <p className="mt-5 border-t border-slate-200 pt-4 text-xs leading-5 text-slate-500">
              Analytics describe patterns in the user's
              historical data and are not medical or clinical
              measurements.
            </p>
          </Card>
        </>
      )}
    </div>
  )
}