import {
  Activity,
  Brain,
  Heart,
  Info,
  Target,
} from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Card from '../../components/ui/Card'
import { wellbeingScores } from '../../mock/wellbeingData'

export default function WellBeingAnalysisPage() {
  const latest = wellbeingScores[wellbeingScores.length - 1]

  const scoreDifference = latest.score - latest.baseline

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="border-b border-slate-200 pb-5">
        <p className="text-sm font-medium text-slate-500">
          Explainable analysis
        </p>

        <h1 className="mt-1 text-2xl font-bold text-slate-800">
          Well-Being Analysis
        </h1>

        <p className="mt-1 max-w-2xl text-sm text-slate-500">
          A transparent view of the signals that contribute to the
          current self-reflection index.
        </p>
      </div>

      {/* Score Overview */}
      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
            <div className="flex h-32 w-32 shrink-0 items-center justify-center rounded-full border-8 border-slate-100">
              <div className="text-center">
                <p className="text-4xl font-bold text-slate-800">
                  {latest.score}
                </p>

                <p className="text-xs text-slate-500">
                  out of 100
                </p>
              </div>
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-semibold text-slate-800">
                  Current Well-Being Index
                </h2>

                <Badge
                  variant={
                    scoreDifference >= 0 ? 'success' : 'warning'
                  }
                >
                  {scoreDifference >= 0 ? '+' : ''}
                  {scoreDifference} vs baseline
                </Badge>
              </div>

              <p className="mt-3 max-w-xl text-sm leading-6 text-slate-600">
                This index combines journal-derived signals and
                habit-related behavioral metrics through the
                MindMirror analysis pipeline.
              </p>

              <div className="mt-4 flex items-start gap-2 rounded-lg bg-slate-50 p-3">
                <Info className="mt-0.5 h-4 w-4 shrink-0 text-slate-500" />

                <p className="text-xs leading-5 text-slate-500">
                  The index is intended for personal reflection and
                  behavioral analytics. It is not a medical or
                  clinical measurement.
                </p>
              </div>
            </div>
          </div>
        </Card>

        <Card title="Personal Baseline">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-slate-100 p-2.5">
              <Activity className="h-5 w-5 text-slate-600" />
            </div>

            <div>
              <p className="text-3xl font-bold text-slate-800">
                {latest.baseline}
              </p>

              <p className="text-xs text-slate-500">
                Current historical reference
              </p>
            </div>
          </div>

          <p className="mt-4 text-sm leading-6 text-slate-600">
            Your baseline is based on your own historical data rather
            than a universal threshold.
          </p>
        </Card>
      </div>

      {/* Input Signals */}
      <Card
        title="Input Signals"
        description="Current numerical signals shown before fuzzy inference."
      >
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <SignalCard
            icon={<Brain className="h-5 w-5" />}
            label="Sentiment"
            value={latest.sentiment}
            description="Journal sentiment signal"
          />

          <SignalCard
            icon={<Heart className="h-5 w-5" />}
            label="Positive Emotion"
            value={latest.positiveEmotion}
            description="Positive emotional signal"
          />

          <SignalCard
            icon={<Activity className="h-5 w-5" />}
            label="Stress Signal"
            value={latest.stress}
            description="Stress-related text signal"
          />

          <SignalCard
            icon={<Target className="h-5 w-5" />}
            label="Habit Consistency"
            value={latest.habitConsistency}
            description="Recent habit consistency"
          />
        </div>
      </Card>

      {/* Explanation */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card
          title="How the analysis works"
          description="High-level explanation of the MindMirror pipeline."
        >
          <div className="space-y-4">
            <AnalysisStep
              number="1"
              title="Journal signals"
              description="Journal text is processed to extract numerical textual and emotional signals."
            />

            <AnalysisStep
              number="2"
              title="Habit metrics"
              description="Habit completion and consistency are converted into numerical behavioral metrics."
            />

            <AnalysisStep
              number="3"
              title="Fuzzy inference"
              description="The numerical signals are provided to the Mamdani fuzzy inference system."
            />

            <AnalysisStep
              number="4"
              title="Well-Being Index"
              description="The fuzzy system produces a 1–100 self-reflection index."
            />
          </div>
        </Card>

        <Card
          title="Current interpretation"
          description="A simple explanation of the displayed values."
        >
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm leading-6 text-slate-600">
              Your latest displayed index is{' '}
              <strong className="font-semibold text-slate-800">
                {latest.score}
              </strong>
              , compared with a personal baseline of{' '}
              <strong className="font-semibold text-slate-800">
                {latest.baseline}
              </strong>
              .
            </p>

            <p className="mt-3 text-sm leading-6 text-slate-600">
              The displayed signals show a sentiment value of{' '}
              <strong className="font-semibold text-slate-800">
                {Math.round(latest.sentiment * 100)}%
              </strong>
              , a positive-emotion signal of{' '}
              <strong className="font-semibold text-slate-800">
                {Math.round(latest.positiveEmotion * 100)}%
              </strong>
              , a stress-related signal of{' '}
              <strong className="font-semibold text-slate-800">
                {Math.round(latest.stress * 100)}%
              </strong>
              , and habit consistency of{' '}
              <strong className="font-semibold text-slate-800">
                {Math.round(latest.habitConsistency * 100)}%
              </strong>
              .
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}

interface SignalCardProps {
  icon: React.ReactNode
  label: string
  value: number
  description: string
}

function SignalCard({
  icon,
  label,
  value,
  description,
}: SignalCardProps) {
  const percentage = Math.round(value * 100)

  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-slate-100 p-2.5 text-slate-600">
          {icon}
        </div>

        <div>
          <p className="text-sm font-medium text-slate-800">
            {label}
          </p>

          <p className="text-xs text-slate-500">
            {description}
          </p>
        </div>
      </div>

      <div className="mt-4 flex items-end justify-between">
        <span className="text-2xl font-bold text-slate-800">
          {percentage}%
        </span>

        <Badge variant="default">Signal</Badge>
      </div>

      <div className="mt-3 h-2 rounded-full bg-slate-100">
        <div
          className="h-2 rounded-full bg-slate-600"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

interface AnalysisStepProps {
  number: string
  title: string
  description: string
}

function AnalysisStep({
  number,
  title,
  description,
}: AnalysisStepProps) {
  return (
    <div className="flex gap-3">
      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-800 text-xs font-semibold text-white">
        {number}
      </div>

      <div>
        <h3 className="text-sm font-semibold text-slate-800">
          {title}
        </h3>

        <p className="mt-1 text-sm leading-5 text-slate-500">
          {description}
        </p>
      </div>
    </div>
  )
}