export interface Habit {
  id: string
  name: string
  targetPerWeek: number
  isActive: boolean
  createdAt: string
}

export interface HabitLog {
  id: string
  habitId: string
  date: string
  completed: boolean
}