import { useEffect, useState } from 'react'
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
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import ChartContainer from '../../components/ui/ChartContainer'
import { analyticsData } from '../../mock/analyticsData'
import { habits, habitLogs } from '../../mock/habitData'
import { insights } from '../../mock/insightData'
import { journalEntries } from '../../mock/journalData'
import { wellbeingScores } from '../../mock/wellbeingData'

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

  const latestScore = wellbeingScores[wellbeingScores.length - 1]
  const latestAnalytics = analyticsData[analyticsData.length - 1]
  const previousScore = wellbeingScores[wellbeingScores.length - 2]

  const scoreChange = latestScore.score - previousScore.score

  const completedLogs = habitLogs.filter((log) => log.completed).length
  const totalLogs = habitLogs.length
  const completionRate = Math.round((completedLogs / totalLogs) * 100)

  const latestInsight = insights[0]

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Personal reflection overview
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-800">
            Good evening
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Here is a snapshot of your recent patterns and progress.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Button variant="secondary">
            <PenLine className="mr-2 h-4 w-4" />
            Write Journal
          </Button>

          <Button>
            <Target className="mr-2 h-4 w-4" />
            View Habits
          </Button>
        </div>
      </div>

      {/* Health Status */}
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
        ) : error ? (
          <Badge variant="error">
            <CircleAlert className="mr-1.5 h-3.5 w-3.5" />
            {error}
          </Badge>
        ) : (
          <Badge variant="info">Checking...</Badge>
        )}
      </div>

      {/* Main Metrics */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Well-Being Index
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {latestScore.score}
              </p>

              <div className="mt-2 flex items-center gap-2">
                <Badge variant="success">
                  <ArrowUpRight className="mr-1 h-3 w-3" />
                  +{scoreChange}
                </Badge>

                <span className="text-xs text-slate-500">
                  since previous entry
                </span>
              </div>
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
                {latestScore.baseline}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Your current historical reference
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
                {completionRate}%
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Across recent tracked days
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
                Recent entries available
              </p>
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <BookOpen className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Trend + Signals */}
      <div className="grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <ChartContainer
            title="Well-Being Trend"
            description="Recent index values compared with your personal baseline."
          >
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={analyticsData}>
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) =>
                    new Date(value).toLocaleDateString('en-IN', {
                      day: 'numeric',
                      month: 'short',
                    })
                  }
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
                  name="Well-Being"
                />

                <Line
                  type="monotone"
                  dataKey="baseline"
                  stroke="#94a3b8"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Baseline"
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>
        </div>

        <Card
          title="Current Signals"
          description="Latest values used by the future analysis pipeline."
        >
          <div className="space-y-5">
            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm text-slate-600">
                  Sentiment
                </span>

                <span className="text-sm font-semibold text-slate-800">
                  {Math.round(latestScore.sentiment * 100)}%
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${latestScore.sentiment * 100}%`,
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
                  {Math.round(latestScore.positiveEmotion * 100)}%
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${latestScore.positiveEmotion * 100}%`,
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
                  {Math.round(latestScore.stress * 100)}%
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${latestScore.stress * 100}%`,
                  }}
                />
              </div>
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm text-slate-600">
                  Habit consistency
                </span>

                <span className="text-sm font-semibold text-slate-800">
                  {Math.round(latestAnalytics.habitConsistency * 100)}%
                </span>
              </div>

              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className="h-2 rounded-full bg-slate-600"
                  style={{
                    width: `${latestAnalytics.habitConsistency * 100}%`,
                  }}
                />
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Habits + Insight */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card
          title="Your Habits"
          description="Recent customizable habits."
        >
          <div className="space-y-3">
            {habits.map((habit) => {
              const habitLogs = habitLogsForHabit(habit.id)

              const completed = habitLogs.filter(
                (log) => log.completed,
              ).length

              return (
                <div
                  key={habit.id}
                  className="flex items-center justify-between rounded-lg border border-slate-200 p-3"
                >
                  <div>
                    <p className="text-sm font-medium text-slate-800">
                      {habit.name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Target: {habit.targetPerWeek} days/week
                    </p>
                  </div>

                  <Badge
                    variant={
                      completed >= Math.ceil(habit.targetPerWeek / 2)
                        ? 'success'
                        : 'warning'
                    }
                  >
                    {completed} completed
                  </Badge>
                </div>
              )
            })}
          </div>
        </Card>

        <Card
          title="Recent Reflection"
          description="An example of an explainable observation."
        >
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div className="flex items-start gap-3">
              <div className="rounded-lg bg-white p-2 shadow-sm">
                <Heart className="h-4 w-4 text-slate-600" />
              </div>

              <div>
                <Badge variant="info">
                  {latestInsight.category}
                </Badge>

                <h3 className="mt-3 text-sm font-semibold text-slate-800">
                  {latestInsight.title}
                </h3>

                <p className="mt-1 text-sm leading-6 text-slate-600">
                  {latestInsight.description}
                </p>
              </div>
            </div>
          </div>

          <Button
            variant="ghost"
            className="mt-4"
          >
            View all insights
          </Button>
        </Card>
      </div>
    </div>
  )
}

function habitLogsForHabit(habitId: string) {
  return habitLogs.filter((log) => log.habitId === habitId)
}