import type { Insight } from "../types/insight";
import InsightCard from "./InsightCard";

interface InsightsPanelProps {
  insights: Insight[];
  title?: string;
}

export default function InsightsPanel({
  insights,
  title = "Self-Reflection Insights",
}: InsightsPanelProps) {
  return (
    <section className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">{title}</h2>

      {insights.length === 0 ? (
        <div className="rounded-xl border border-gray-200 bg-white p-6 text-center">
          <p className="text-sm text-gray-500">
            No meaningful patterns have been identified yet.
          </p>
        </div>
      ) : (
        <div className="grid gap-4">
          {insights.map((insight) => (
            <InsightCard key={insight.insight_key} insight={insight} />
          ))}
        </div>
      )}
    </section>
  );
}