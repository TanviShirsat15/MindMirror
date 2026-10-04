export interface Habit {
  id: number
  user_id: number
  name: string
  target_value: number
  target_unit: string | null
  frequency: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface HabitLog {
  id: number
  habit_id: number
  user_id: number
  log_date: string
  completed_value: number | null
  is_completed: boolean
  created_at: string
  updated_at: string
}

export interface HabitMetrics {
  habit_id: number
  window: 'weekly' | 'historical'
  start_date: string
  end_date: string
  expected_days: number
  completed_days: number
  completion_rate: number
  current_streak: number
  longest_streak: number
}