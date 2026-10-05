export type InsightCategory =
  | 'baseline'
  | 'trend'
  | 'habit'
  | 'emotional'
  | 'consistency'
  | 'recent-change'

export type InsightDirection =
  | 'positive'
  | 'negative'
  | 'neutral'

export interface Insight {
  insight_key: string
  category: InsightCategory
  subject: string
  title: string
  explanation: string
  direction: InsightDirection
  supporting_metrics: Record<string, unknown>
  comparison_period: string | null
  data_sufficiency: string
  sample_size: number
  is_new: boolean
  first_generated_at: string | null
  generated_at: string
}

export interface GeneratedInsightsResponse {
  status: 'success'
  as_of: string
  generated_at: string
  insights: Insight[]
  meta: {
    disclaimer: string
  }
}