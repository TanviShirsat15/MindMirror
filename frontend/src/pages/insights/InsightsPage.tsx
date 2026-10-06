import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import {
  Activity,
  ArrowUpRight,
  CalendarDays,
  CheckCircle2,
  Heart,
  Lightbulb,
  TrendingUp,
} from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Card from '../../components/ui/Card'
import EmptyState from '../../components/ui/EmptyState'
import { apiGet } from '../../api/client'

const categoryLabels: Record<string, string> = {
  baseline: 'Baseline',
  trend: 'Trend',
  habit: 'Habit',
  emotional: 'Emotional',
  consistency: 'Consistency',
  'recent-change': 'Recent Change',
}

interface GeneratedInsight {
  insight_key: string
  category: string
  subject: string
  title: string
  explanation: string
  direction: string
  supporting_metrics: Record<string, unknown>
  comparison_period: string | null
  data_sufficiency: string
  sample_size: number
  is_new: boolean
  first_generated_at: string | null
  generated_at: string
}

interface GeneratedInsightsResponse {
  status: string
  as_of: string
  generated_at: string
  insights: GeneratedInsight[]
  meta: {
    disclaimer: string
  }
}

function formatCategory(category: string): string {
  return (
    categoryLabels[category] ??
    category
      .replace(/[-_]/g, ' ')
      .replace(/\b\w/g, (letter) => letter.toUpperCase())
  )
}

function formatDate(value: string | null): string {
  if (!value) {
    return 'Date unavailable'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return 'Date unavailable'
  }

  return date.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

function formatDirection(direction: string): string {
  return direction
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function formatMetricValue(value: unknown): string {
  if (typeof value === 'number') {
    if (Number.isInteger(value)) {
      return String(value)
    }

    return value.toFixed(2)
  }

  if (typeof value === 'string') {
    return value
  }

  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No'
  }

  return String(value)
}

function getSupportingMetrics(
  metrics: Record<string, unknown>,
): Array<[string, unknown]> {
  return Object.entries(metrics).filter(
    ([key, value]) =>
      key !== 'threshold' &&
      value !== null &&
      value !== undefined,
  )
}

export default function InsightsPage() {
  const [data, setData] = useState<GeneratedInsightsResponse | null>(
    null,
  )
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    setLoading(true)
    setError(null)

    apiGet<GeneratedInsightsResponse>('/api/insights/generated')
      .then((response) => {
        if (!active) {
          return
        }

        setData(response)
      })
      .catch(() => {
        if (!active) {
          return
        }

        setError(
          'Insights could not be loaded. Please try again.',
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
  }, [])

  if (loading) {
    return (
      <div className="p-6 text-sm text-slate-500">
        Loading insights...
      </div>
    )
  }

  if (error) {
    return (
      <Card title="Insights">
        <p className="text-sm text-red-600">{error}</p>
      </Card>
    )
  }

  const insights = data?.insights ?? []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 pb-5">
        <p className="text-sm font-medium text-slate-500">
          Explainable observations
        </p>

        <h1 className="mt-1 text-2xl font-bold text-slate-800">
          Insights
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-slate-500">
          Explore patterns observed across your journal signals,
          habits, and personal well-being history.
        </p>
      </div>

      {/* Intro */}
      <Card>
        <div className="flex items-start gap-4">
          <div className="rounded-xl bg-slate-100 p-3">
            <Lightbulb className="h-5 w-5 text-slate-600" />
          </div>

          <div>
            <h2 className="text-base font-semibold text-slate-800">
              Your reflection patterns
            </h2>

            <p className="mt-1 text-sm leading-6 text-slate-500">
              {data?.meta.disclaimer ??
                'These observations are based on patterns in your own historical data.'}
            </p>
          </div>
        </div>
      </Card>

      {/* Generated Insights */}
      {insights.length === 0 ? (
        <EmptyState
          title="No insights available"
          description="Insights will appear as enough historical data becomes available."
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {insights.map((insight) => (
            <InsightCard
              key={insight.insight_key}
              insight={insight}
            />
          ))}
        </div>
      )}

      {/* Categories */}
      <Card
        title="Insight categories"
        description="The different types of observations MindMirror can present."
      >
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <CategoryItem
            icon={<Activity className="h-4 w-4" />}
            title="Baseline"
            description="Compares recent values with your personal historical reference."
          />

          <CategoryItem
            icon={<TrendingUp className="h-4 w-4" />}
            title="Trend"
            description="Highlights changes across your recent history."
          />

          <CategoryItem
            icon={<CheckCircle2 className="h-4 w-4" />}
            title="Habit"
            description="Shows observed associations between habits and other signals."
          />

          <CategoryItem
            icon={<Heart className="h-4 w-4" />}
            title="Emotional"
            description="Describes changes in journal-derived emotional signals."
          />

          <CategoryItem
            icon={<CalendarDays className="h-4 w-4" />}
            title="Consistency"
            description="Highlights patterns in routine and habit consistency."
          />

          <CategoryItem
            icon={<ArrowUpRight className="h-4 w-4" />}
            title="Recent Change"
            description="Points out noticeable changes in the latest displayed data."
          />
        </div>
      </Card>
    </div>
  )
}

interface InsightCardProps {
  insight: GeneratedInsight
}

function InsightCard({ insight }: InsightCardProps) {
  const supportingMetrics = getSupportingMetrics(
    insight.supporting_metrics,
  )

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="info">
            {formatCategory(insight.category)}
          </Badge>

          {insight.is_new && (
            <Badge variant="success">
              New
            </Badge>
          )}
        </div>

        <span className="text-xs text-slate-400">
          {formatDate(insight.generated_at)}
        </span>
      </div>

      <h2 className="mt-4 text-base font-semibold text-slate-800">
        {insight.title}
      </h2>

      <p className="mt-2 text-sm leading-6 text-slate-600">
        {insight.explanation}
      </p>

      <div className="mt-4 grid gap-3 border-t border-slate-100 pt-4 sm:grid-cols-2">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Direction
          </p>

          <p className="mt-1 text-sm font-medium text-slate-700">
            {formatDirection(insight.direction)}
          </p>
        </div>

        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Sample size
          </p>

          <p className="mt-1 text-sm font-medium text-slate-700">
            {insight.sample_size}
          </p>
        </div>

        {insight.comparison_period && (
          <div className="sm:col-span-2">
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
              Comparison period
            </p>

            <p className="mt-1 text-sm text-slate-700">
              {insight.comparison_period}
            </p>
          </div>
        )}
      </div>

      {supportingMetrics.length > 0 && (
        <div className="mt-4 rounded-lg bg-slate-50 p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Supporting information
          </p>

          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            {supportingMetrics.map(([key, value]) => (
              <div
                key={key}
                className="flex items-center justify-between gap-3 text-sm"
              >
                <span className="text-slate-500">
                  {key
                    .replace(/[-_]/g, ' ')
                    .replace(/\b\w/g, (letter) =>
                      letter.toUpperCase(),
                    )}
                </span>

                <span className="font-medium text-slate-700">
                  {formatMetricValue(value)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </article>
  )
}

interface CategoryItemProps {
  icon: ReactNode
  title: string
  description: string
}

function CategoryItem({
  icon,
  title,
  description,
}: CategoryItemProps) {
  return (
    <div className="rounded-lg border border-slate-200 p-4">
      <div className="flex items-center gap-2">
        <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
          {icon}
        </div>

        <h3 className="text-sm font-semibold text-slate-800">
          {title}
        </h3>
      </div>

      <p className="mt-2 text-sm leading-5 text-slate-500">
        {description}
      </p>
    </div>
  )
}