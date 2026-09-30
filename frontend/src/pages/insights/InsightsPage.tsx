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
import { insights } from '../../mock/insightData'

const categoryLabels = {
  baseline: 'Baseline',
  trend: 'Trend',
  habit: 'Habit',
  emotional: 'Emotional',
  consistency: 'Consistency',
  'recent-change': 'Recent Change',
}

export default function InsightsPage() {
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
              These observations are based on patterns in your own
              historical data. They describe associations and trends
              rather than diagnoses or cause-and-effect relationships.
            </p>
          </div>
        </div>
      </Card>

      {/* Insight Cards */}
      {insights.length === 0 ? (
        <EmptyState
          title="No insights available"
          description="Insights will appear as enough historical data becomes available."
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {insights.map((insight) => (
            <InsightCard
              key={insight.id}
              category={insight.category}
              title={insight.title}
              description={insight.description}
              createdAt={insight.createdAt}
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
  category: keyof typeof categoryLabels
  title: string
  description: string
  createdAt: string
}

function InsightCard({
  category,
  title,
  description,
  createdAt,
}: InsightCardProps) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <Badge variant="info">
          {categoryLabels[category]}
        </Badge>

        <span className="text-xs text-slate-400">
          {new Date(createdAt).toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
          })}
        </span>
      </div>

      <h2 className="mt-4 text-base font-semibold text-slate-800">
        {title}
      </h2>

      <p className="mt-2 text-sm leading-6 text-slate-600">
        {description}
      </p>
    </article>
  )
}

interface CategoryItemProps {
  icon: React.ReactNode
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