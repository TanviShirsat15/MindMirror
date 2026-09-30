import { useMemo, useState } from 'react'

import {
  Activity,
  BarChart3,
  CalendarDays,
  TrendingDown,
  TrendingUp,
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

import Badge from '../../components/ui/Badge'
import Card from '../../components/ui/Card'
import ChartContainer from '../../components/ui/ChartContainer'
import { analyticsData } from '../../mock/analyticsData'

type TimeRange = '7' | '5'

export default function AnalyticsHistoryPage() {
  const [timeRange, setTimeRange] = useState<TimeRange>('7')

  const filteredData = useMemo(() => {
    if (timeRange === '5') {
      return analyticsData.slice(-5)
    }

    return analyticsData
  }, [timeRange])

  const latest = filteredData[filteredData.length - 1]
  const previous = filteredData[filteredData.length - 2]

  const scoreChange = latest.score - previous.score

  const averageScore = Math.round(
    filteredData.reduce((sum, point) => sum + point.score, 0) /
      filteredData.length,
  )

  const averageHabitConsistency = Math.round(
    (filteredData.reduce(
      (sum, point) => sum + point.habitConsistency,
      0,
    ) /
      filteredData.length) *
      100,
  )

  const averageSentiment = Math.round(
    (filteredData.reduce(
      (sum, point) => sum + point.sentiment,
      0,
    ) /
      filteredData.length) *
      100,
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Personal history
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-800">
            Analytics & History
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Explore changes in your personal signals and well-being
            index over time.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <CalendarDays className="h-4 w-4 text-slate-400" />

          <select
            value={timeRange}
            onChange={(event) =>
              setTimeRange(event.target.value as TimeRange)
            }
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-100"
            aria-label="Select analytics time range"
          >
            <option value="7">Recent 7 entries</option>
            <option value="5">Recent 5 entries</option>
          </select>
        </div>
      </div>

      {/* Summary Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Average Index
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {averageScore}
              </p>
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <BarChart3 className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-500">
                Latest Change
              </p>

              <p className="mt-2 text-3xl font-bold text-slate-800">
                {scoreChange >= 0 ? '+' : ''}
                {scoreChange}
              </p>

              <div className="mt-2">
                <Badge
                  variant={scoreChange >= 0 ? 'success' : 'warning'}
                >
                  {scoreChange >= 0 ? (
                    <TrendingUp className="mr-1 h-3 w-3" />
                  ) : (
                    <TrendingDown className="mr-1 h-3 w-3" />
                  )}
                  Recent change
                </Badge>
              </div>
            </div>

            <div className="rounded-lg bg-slate-100 p-2.5">
              <Activity className="h-5 w-5 text-slate-600" />
            </div>
          </div>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Avg. Habit Consistency
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-800">
            {averageHabitConsistency}%
          </p>

          <p className="mt-2 text-xs text-slate-500">
            Across the selected period
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Avg. Sentiment
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-800">
            {averageSentiment}%
          </p>

          <p className="mt-2 text-xs text-slate-500">
            Journal-related signal
          </p>
        </Card>
      </div>

      {/* Main Well-Being Chart */}
      <ChartContainer
        title="Well-Being Index Trend"
        description="Current index compared with your personal baseline."
      >
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={filteredData}>
            <CartesianGrid strokeDasharray="3 3" />

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

            <Legend />

            <Line
              type="monotone"
              dataKey="score"
              stroke="#334155"
              strokeWidth={2.5}
              dot={{ r: 3 }}
              name="Well-Being Index"
            />

            <Line
              type="monotone"
              dataKey="baseline"
              stroke="#94a3b8"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              name="Personal Baseline"
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      {/* Signal Charts */}
      <div className="grid gap-6 lg:grid-cols-2">
        <ChartContainer
          title="Habit Consistency"
          description="Recent consistency values across the selected period."
        >
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />

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
                domain={[0, 1]}
                tick={{ fontSize: 12 }}
                tickFormatter={(value) =>
                  `${Math.round(value * 100)}%`
                }
              />

              <Tooltip
                formatter={(value) =>
                  `${Math.round(Number(value) * 100)}%`
                }
              />

              <Line
                type="monotone"
                dataKey="habitConsistency"
                stroke="#475569"
                strokeWidth={2.5}
                dot={{ r: 3 }}
                name="Habit Consistency"
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer
          title="Journal Signals"
          description="Sentiment and stress-related signals from the displayed period."
        >
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />

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
                domain={[0, 1]}
                tick={{ fontSize: 12 }}
                tickFormatter={(value) =>
                  `${Math.round(value * 100)}%`
                }
              />

              <Tooltip
                formatter={(value) =>
                  `${Math.round(Number(value) * 100)}%`
                }
              />

              <Legend />

              <Line
                type="monotone"
                dataKey="sentiment"
                stroke="#334155"
                strokeWidth={2}
                dot={{ r: 3 }}
                name="Sentiment"
              />

              <Line
                type="monotone"
                dataKey="stress"
                stroke="#94a3b8"
                strokeWidth={2}
                dot={{ r: 3 }}
                name="Stress Signal"
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      {/* Supporting Information */}
      <Card
        title="How to read these trends"
        description="The charts describe your own historical patterns."
      >
        <div className="grid gap-4 text-sm text-slate-600 md:grid-cols-3">
          <div className="rounded-lg bg-slate-50 p-4">
            <p className="font-semibold text-slate-800">
              Personal baseline
            </p>

            <p className="mt-1 leading-5">
              Your baseline provides a historical reference based on
              your own data.
            </p>
          </div>

          <div className="rounded-lg bg-slate-50 p-4">
            <p className="font-semibold text-slate-800">
              Journal signals
            </p>

            <p className="mt-1 leading-5">
              Sentiment and stress-related values represent extracted
              text signals, not diagnoses.
            </p>
          </div>

          <div className="rounded-lg bg-slate-50 p-4">
            <p className="font-semibold text-slate-800">
              Historical patterns
            </p>

            <p className="mt-1 leading-5">
              Trends describe observed changes and should not be
              interpreted as proof of cause and effect.
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}