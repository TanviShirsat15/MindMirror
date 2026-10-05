import { useEffect, useState } from "react";
import InsightCard from "../../components/InsightCard";
import { apiGet } from "../../api/client";
import type { GeneratedInsightsResponse } from "../../types/insight";

export default function InsightsPage() {
  const [data, setData] = useState<GeneratedInsightsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    apiGet<GeneratedInsightsResponse>("/api/insights/generated")
      .then((result) => {
        setData(result);
      })
      .catch(() => {
        setError(true);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="h-6 w-48 animate-pulse rounded bg-gray-200" />
        <div className="mt-4 h-24 animate-pulse rounded-xl bg-gray-200" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <h1 className="text-xl font-semibold text-gray-900">
          Self-Reflection Insights
        </h1>
        <p className="mt-3 text-sm text-gray-600">
          Unable to load insights. Please try again.
        </p>
      </div>
    );
  }

  if (!data || data.insights.length === 0) {
    return (
      <div className="p-6">
        <h1 className="text-xl font-semibold text-gray-900">
          Self-Reflection Insights
        </h1>
        <p className="mt-3 text-sm text-gray-500">
          No meaningful patterns have been identified yet.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-xl font-semibold text-gray-900">
          Self-Reflection Insights
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Patterns identified from your own historical data.
        </p>
      </div>

      <div className="grid gap-4">
        {data.insights.map((insight) => (
          <InsightCard
            key={insight.insight_key}
            insight={insight}
          />
        ))}
      </div>

      <p className="text-xs leading-5 text-gray-500">
        {data.meta.disclaimer}
      </p>
    </div>
  );
}