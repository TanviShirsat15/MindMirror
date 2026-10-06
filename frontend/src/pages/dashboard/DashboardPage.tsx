import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import {
  Activity,
  ArrowUpRight,
  BookOpen,
  CheckCircle2,
  CircleAlert,
  Heart,
  PenLine,
  Target,
} from 'lucide-react'

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import Badge from '../../components/ui/Badge'
import Card from '../../components/ui/Card'
import ChartContainer from '../../components/ui/ChartContainer'
import { apiGet } from '../../api/client'
import type { GeneratedInsightsResponse } from '../../types/insight'

interface HealthStatus {
  status: string
  db: string
}

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

interface AnalyticsMeta {
  start_date: string
  end_date: string
  granularity: 'daily' | 'weekly' | 'monthly'
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

interface AnalyticsWellBeingResponse {
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

interface AnalyticsHabitResponse {
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

interface NLPResponse {
  meta: AnalyticsMeta
  data: NLPPoint[]
}

interface Habit {
  id: number
  name: string
  target_value: number
  target_unit: string | null
  frequency: string
  is_active: boolean
}

interface JournalEntry {
  id: number
  user_id: number
  content: string
  entry_date: string
  created_at: string
  updated_at: string
}

function getTodayDate(): string {
  const today = new Date()

  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function getDateDaysAgo(days: number): string {
  const date = new Date()
  date.setDate(date.getDate() - days)

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function formatDate(dateString: string): string {
  const [year, month, day] = dateString.split('-').map(Number)

  if (!year || !month || !day) {
    return dateString
  }

  return new Date(year, month - 1, day).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
  })
}

function formatChartDate(value: string | undefined): string {
  if (!value) {
    return ''
  }

  return new Date(`${value}T00:00:00`).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
  })
}

function truncateText(value: string, maxLength = 180): string {
  const normalized = value.trim().replace(/\s+/g, ' ')

  if (normalized.length <= maxLength) {
    return normalized
  }

  return `${normalized.slice(0, maxLength).trim()}...`
}

function getComparisonLabel(
  comparison: WellBeingResponse['comparison'],
): string {
  if (comparison === 'above') {
    return 'Above baseline'
  }

  if (comparison === 'below') {
    return 'Below baseline'
  }

  if (comparison === 'near') {
    return 'Near baseline'
  }

  return 'Baseline unavailable'
}

function getComparisonVariant(
  comparison: WellBeingResponse['comparison'],
): 'success' | 'warning' | 'default' {
  if (comparison === 'above') {
    return 'success'
  }

  if (comparison === 'below') {
    return 'warning'
  }

  return 'default'
}

export default function DashboardPage() {
  const today = getTodayDate()
  const sevenDaysAgo = getDateDaysAgo(6)
  const thirtyDaysAgo = getDateDaysAgo(29)

  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)

  const [wellbeing, setWellbeing] =
    useState<WellBeingResponse | null>(null)

  const [wellbeingAnalytics, setWellbeingAnalytics] =
    useState<AnalyticsWellBeingResponse | null>(null)

  const [habitAnalytics, setHabitAnalytics] =
    useState<AnalyticsHabitResponse | null>(null)

  const [nlp, setNlp] = useState<NLPResponse | null>(null)

  const [habits, setHabits] = useState<Habit[]>([])
  const [journalEntries, setJournalEntries] =
    useState<JournalEntry[]>([])

  const [generatedInsights, setGeneratedInsights] =
    useState<GeneratedInsightsResponse | null>(null)

  const [loading, setLoading] = useState(true)
  const [dashboardError, setDashboardError] =
    useState<string | null>(null)

  useEffect(() => {
    let active = true

    async function loadDashboard() {
      setLoading(true)
      setDashboardError(null)

      const results = await Promise.allSettled([
        apiGet<WellBeingResponse>(`/api/wellbeing/${today}`),

        apiGet<AnalyticsWellBeingResponse>(
          `/api/analytics/wellbeing?start_date=${thirtyDaysAgo}&end_date=${today}&granularity=daily`,
        ),

        apiGet<AnalyticsHabitResponse>(
          `/api/analytics/habits?start_date=${sevenDaysAgo}&end_date=${today}&granularity=weekly`,
        ),

        apiGet<NLPResponse>(
          `/api/analytics/nlp?start_date=${today}&end_date=${today}&granularity=daily`,
        ),

        apiGet<Habit[]>('/api/habits'),

        apiGet<JournalEntry[]>('/api/journals'),

        apiGet<GeneratedInsightsResponse>(
          '/api/insights/generated',
        ),
      ])

      if (!active) {
        return
      }

      const [
        wellbeingResult,
        wellbeingAnalyticsResult,
        habitAnalyticsResult,
        nlpResult,
        habitsResult,
        journalsResult,
        insightsResult,
      ] = results

      let successfulRequests = 0

      if (wellbeingResult.status === 'fulfilled') {
        setWellbeing(wellbeingResult.value)
        successfulRequests += 1
      } else {
        setWellbeing(null)
      }

      if (wellbeingAnalyticsResult.status === 'fulfilled') {
        setWellbeingAnalytics(wellbeingAnalyticsResult.value)
        successfulRequests += 1
      } else {
        setWellbeingAnalytics(null)
      }

      if (habitAnalyticsResult.status === 'fulfilled') {
        setHabitAnalytics(habitAnalyticsResult.value)
        successfulRequests += 1
      } else {
        setHabitAnalytics(null)
      }

      if (nlpResult.status === 'fulfilled') {
        setNlp(nlpResult.value)
        successfulRequests += 1
      } else {
        setNlp(null)
      }

      if (habitsResult.status === 'fulfilled') {
        setHabits(habitsResult.value)
        successfulRequests += 1
      } else {
        setHabits([])
      }

      if (journalsResult.status === 'fulfilled') {
        setJournalEntries(journalsResult.value)
        successfulRequests += 1
      } else {
        setJournalEntries([])
      }

      if (insightsResult.status === 'fulfilled') {
        setGeneratedInsights(insightsResult.value)
        successfulRequests += 1
      } else {
        setGeneratedInsights(null)
      }

      if (successfulRequests === 0) {
        setDashboardError(
          'Dashboard data could not be loaded. Please try again.',
        )
      }

      setLoading(false)
    }

    void loadDashboard()

    return () => {
      active = false
    }
  }, [today, sevenDaysAgo, thirtyDaysAgo])

  useEffect(() => {
    let active = true

    async function checkHealth() {
      try {
        const response = await fetch('/api/health')

        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`)
        }

        const data: HealthStatus = await response.json()

        if (active) {
          setHealth(data)
          setHealthError(null)
        }
      } catch {
        if (active) {
          setHealth(null)
          setHealthError('Backend unreachable')
        }
      }
    }

    void checkHealth()

    return () => {
      active = false
    }
  }, [])

  const sortedJournalEntries = useMemo(() => {
    return [...journalEntries].sort((a, b) => {
      const dateDifference =
        new Date(`${b.entry_date}T00:00:00`).getTime() -
        new Date(`${a.entry_date}T00:00:00`).getTime()

      if (dateDifference !== 0) {
        return dateDifference
      }

      return (
        new Date(b.created_at).getTime() -
        new Date(a.created_at).getTime()
      )
    })
  }, [journalEntries])

  const recentJournal = sortedJournalEntries[0] ?? null

  const latestInsight = generatedInsights?.insights[0] ?? null

  const latestNlp = nlp?.data.find(
    (point) => point.date === today,
  )

  const latestHabitPoint =
    habitAnalytics?.data[habitAnalytics.data.length - 1] ?? null

  const wellbeingChartData = useMemo(() => {
    return (
      wellbeingAnalytics?.data.map((point) => ({
        date: point.date,
        label: formatChartDate(point.date),
        score: point.score,
        baseline: point.baseline,
      })) ?? []
    )
  }, [wellbeingAnalytics])

  const recentAverage = wellbeingAnalytics?.summary.average ?? null

  const habitCompletion =
    latestHabitPoint?.completion_rate ?? null

  const sentiment = latestNlp?.sentiment ?? null
  const positiveEmotion = latestNlp?.positive_emotion ?? null
  const stress = latestNlp?.stress ?? null

  const sentimentBarValue =
    sentiment === null
      ? 0
      : Math.max(0, Math.min(100, ((sentiment + 1) / 2) * 100))

  const positiveEmotionBarValue =
    positiveEmotion === null
      ? 0
      : Math.max(0, Math.min(100, positiveEmotion * 100))

  const stressBarValue =
    stress === null
      ? 0
      : Math.max(0, Math.min(100, stress * 100))

  if (loading) {
    return (
      <div className="p-6 text-sm text-slate-500">
        Loading dashboard...
      </div>
    )
  }

  if (dashboardError) {
    return (
      <Card title="Dashboard unavailable">
        <p className="text-sm leading-6 text-slate-500">
          {dashboardError}
        </p>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Personal reflection overview
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-800">
            Your Dashboard
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Here is a snapshot of your recent patterns and progress.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Link
            to="/journal"
            className="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
          >
            <PenLine className="mr-2 h-4 w-4" />
            Write Journal
          </Link>

          <Link
            to="/habits"
            className="inline-flex items-center justify-center rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2"
          >
            <Target className="mr-2 h-4 w-4" />
            View Habits
          </Link>
        </div>
      </div>

      <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
        <div className="flex items-center gap-2 text-sm text-slate-600">
          <Activity className="h-4 w-4 text-slate-400" />
          <span>System status</span>
        </div>

        {health ? (
          <Badge variant="success">
            <CheckCircle2 className="mr-1.5 h-3.5 w-3.5" />
            Backend connected · DB {health.db}
          </Badge>
        ) : healthError ? (
          <Badge variant="error">
            <CircleAlert className="mr-1.5 h-3.5 w-3.5" />
            {healthError}
          </Badge>
        ) : (
          <Badge variant="info">Checking...</Badge>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Well-Being Index
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {wellbeing ? wellbeing.score : '—'}
              </p>

              {wellbeing?.comparison && (
                <div className="mt-2 flex items-center gap-2">
                  <Badge
                    variant={getComparisonVariant(
                      wellbeing.comparison,
                    )}
                  >
                    {wellbeing.difference !== null &&
                    wellbeing.difference >= 0
                      ? '+'
                      : ''}
                    {wellbeing.difference ?? '—'} vs baseline
                  </Badge>

                  <span className="text-xs text-slate-500">
                    {getComparisonLabel(wellbeing.comparison)}
                  </span>
                </div>
              )}

              {!wellbeing && (
                <p className="mt-2 text-xs text-slate-500">
                  No well-being score is available for today.
                </p>
              )}

              {wellbeing?.status === 'insufficient_history' && (
                <p className="mt-2 text-xs text-slate-500">
                  Your personal baseline is still being built.
                </p>
              )}
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <Heart className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Personal Baseline
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {wellbeing?.baseline !== null &&
                wellbeing?.baseline !== undefined
                  ? wellbeing.baseline.toFixed(1)
                  : '—'}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                {wellbeing?.baseline_sample_size
                  ? `Based on ${wellbeing.baseline_sample_size} previous scores`
                  : 'Historical reference from your own data'}
              </p>
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <Activity className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Habit Completion
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {habitCompletion !== null
                  ? `${Math.round(habitCompletion * 100)}%`
                  : '—'}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Last 7 calendar days
              </p>
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <Target className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Journal Entries
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {journalEntries.length}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Stored entries
              </p>
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <BookOpen className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <ChartContainer
            title="Well-Being Trend"
            description="Recent index values compared with your personal baseline."
          >
            {wellbeingChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
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

                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#334155"
                    strokeWidth={2.5}
                    dot={{ r: 3 }}
                    connectNulls={false}
                    name="Well-Being"
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
            ) : (
              <div className="flex h-[280px] items-center justify-center text-sm text-slate-500">
                No historical well-being scores are available for this period.
              </div>
            )}
          </ChartContainer>
        </div>

        <Card
          title="Current Signals"
          description="Latest journal-derived signals available from your stored analysis."
        >
          <div className="space-y-5">
            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm text-slate-600">
                  Sentiment signal
                </span>

                <span className="text-sm font-semibold text-slate-800">
                  {sentiment !== null
                    ? sentiment.toFixed(2)
                    : '—'}
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${sentimentBarValue}%`,
                  }}
                />
              </div>
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm text-slate-600">
                  Positive emotion
                </span>

                <span className="text-sm font-semibold text-slate-800">
                  {positiveEmotion !== null
                    ? `${Math.round(positiveEmotion * 100)}%`
                    : '—'}
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${positiveEmotionBarValue}%`,
                  }}
                />
              </div>
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm text-slate-600">
                  Stress-related signal
                </span>

                <span className="text-sm font-semibold text-slate-800">
                  {stress !== null
                    ? `${Math.round(stress * 100)}%`
                    : '—'}
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${stressBarValue}%`,
                  }}
                />
              </div>
            </div>

            {!latestNlp && (
              <p className="text-xs leading-5 text-slate-500">
                No journal analysis is available for today yet.
              </p>
            )}
          </div>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">
                Recent Average
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {recentAverage !== null
                  ? recentAverage.toFixed(1)
                  : '—'}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Based on available scored days in the selected history window.
              </p>
            </div>

            <ArrowUpRight className="h-5 w-5 text-slate-400" />
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">
                Available Habits
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {habits.filter((habit) => habit.is_active).length}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Active habits currently tracked.
              </p>
            </div>

            <Target className="h-5 w-5 text-slate-400" />
          </div>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card
          title="Your Habits"
          description="Your currently active habits from the database."
        >
          {habits.filter((habit) => habit.is_active).length === 0 ? (
            <p className="text-sm leading-6 text-slate-500">
              No active habits are available yet.
            </p>
          ) : (
            <div className="space-y-3">
              {habits
                .filter((habit) => habit.is_active)
                .map((habit) => (
                  <div
                    key={habit.id}
                    className="flex items-center justify-between rounded-lg border border-slate-200 p-3"
                  >
                    <div>
                      <p className="text-sm font-medium text-slate-800">
                        {habit.name}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        Target: {habit.target_value}
                        {habit.target_unit
                          ? ` ${habit.target_unit}`
                          : ''}{' '}
                        {habit.frequency}
                      </p>
                    </div>

                    <Badge variant="success">
                      Active
                    </Badge>
                  </div>
                ))}
            </div>
          )}

          <Link
            to="/habits"
            className="mt-4 inline-flex items-center justify-center rounded-lg bg-transparent px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
          >
            Manage habits
          </Link>
        </Card>

        <Card
          title="Recent Reflection"
          description="Your latest stored journal entry."
        >
          {recentJournal ? (
            <>
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                <div className="flex items-start gap-3">
                  <div className="rounded-lg bg-white p-2 shadow-sm">
                    <Heart className="h-4 w-4 text-slate-600" />
                  </div>

                  <div className="min-w-0">
                    <p className="text-xs font-medium text-slate-500">
                      {formatDate(recentJournal.entry_date)}
                    </p>

                    <p className="mt-2 text-sm leading-6 text-slate-600">
                      {truncateText(recentJournal.content)}
                    </p>
                  </div>
                </div>
              </div>

              <Link
                to="/journal"
                className="mt-4 inline-flex items-center justify-center rounded-lg bg-transparent px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
              >
                View journal
              </Link>
            </>
          ) : (
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm leading-6 text-slate-500">
                No journal entries are available yet.
              </p>

              <Link
                to="/journal"
                className="mt-4 inline-flex items-center justify-center rounded-lg bg-slate-800 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2"
              >
                <PenLine className="mr-2 h-4 w-4" />
                Write your first journal
              </Link>
            </div>
          )}
        </Card>
      </div>

      <Card
        title="Recent Insight"
        description="The latest explainable observation generated from your real data."
      >
        {latestInsight ? (
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div className="flex items-start gap-3">
              <div className="rounded-lg bg-white p-2 shadow-sm">
                <Heart className="h-4 w-4 text-slate-600" />
              </div>

              <div className="min-w-0">
                <Badge variant="info">
                  {latestInsight.category}
                </Badge>

                <h3 className="mt-3 text-sm font-semibold text-slate-800">
                  {latestInsight.title}
                </h3>

                <p className="mt-1 text-sm leading-6 text-slate-600">
                  {latestInsight.explanation}
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm leading-6 text-slate-500">
              No explainable insight is available yet. Insights will appear
              when enough meaningful historical data is available.
            </p>
          </div>
        )}

        <Link
          to="/insights"
          className="mt-4 inline-flex items-center justify-center rounded-lg bg-transparent px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
        >
          View all insights
        </Link>
      </Card>
    </div>
  )
}