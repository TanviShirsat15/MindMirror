import type { Insight } from "../types/insight";

interface InsightCardProps {
  insight: Insight;
}

export default function InsightCard({ insight }: InsightCardProps) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <div className="mb-2 flex items-center justify-between gap-3">
        <span className="text-xs font-medium uppercase tracking-wide text-gray-500">
          {insight.category}
        </span>

        {insight.is_new && (
          <span className="rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-600">
            New
          </span>
        )}
      </div>

      <h3 className="text-base font-semibold text-gray-900">
        {insight.title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-gray-600">
        {insight.explanation}
      </p>

      <p className="mt-3 text-xs text-gray-500">
        Based on {insight.sample_size} data point
        {insight.sample_size !== 1 ? "s" : ""}.
      </p>
    </div>
  );
}