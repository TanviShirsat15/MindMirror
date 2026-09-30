export type InsightCategory =
  | 'baseline'
  | 'trend'
  | 'habit'
  | 'emotional'
  | 'consistency'
  | 'recent-change'

export interface Insight {
  id: string
  category: InsightCategory
  title: string
  description: string
  createdAt: string
}