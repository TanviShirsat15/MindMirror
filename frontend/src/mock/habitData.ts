import type { Habit, HabitLog } from '../types/habit'

export const habits: Habit[] = [
  {
    id: 'habit-1',
    name: 'Exercise',
    targetPerWeek: 4,
    isActive: true,
    createdAt: '2026-09-01T09:00:00',
  },
  {
    id: 'habit-2',
    name: 'Reading',
    targetPerWeek: 5,
    isActive: true,
    createdAt: '2026-09-01T09:15:00',
  },
  {
    id: 'habit-3',
    name: 'Study',
    targetPerWeek: 6,
    isActive: true,
    createdAt: '2026-09-02T08:30:00',
  },
  {
    id: 'habit-4',
    name: 'Meditation',
    targetPerWeek: 3,
    isActive: true,
    createdAt: '2026-09-03T07:45:00',
  },
]

export const habitLogs: HabitLog[] = [
  {
    id: 'log-1',
    habitId: 'habit-1',
    date: '2026-09-28',
    completed: true,
  },
  {
    id: 'log-2',
    habitId: 'habit-1',
    date: '2026-09-29',
    completed: false,
  },
  {
    id: 'log-3',
    habitId: 'habit-1',
    date: '2026-09-30',
    completed: true,
  },
  {
    id: 'log-4',
    habitId: 'habit-2',
    date: '2026-09-28',
    completed: true,
  },
  {
    id: 'log-5',
    habitId: 'habit-2',
    date: '2026-09-29',
    completed: true,
  },
  {
    id: 'log-6',
    habitId: 'habit-2',
    date: '2026-09-30',
    completed: true,
  },
  {
    id: 'log-7',
    habitId: 'habit-3',
    date: '2026-09-28',
    completed: true,
  },
  {
    id: 'log-8',
    habitId: 'habit-3',
    date: '2026-09-29',
    completed: true,
  },
  {
    id: 'log-9',
    habitId: 'habit-3',
    date: '2026-09-30',
    completed: false,
  },
  {
    id: 'log-10',
    habitId: 'habit-4',
    date: '2026-09-28',
    completed: false,
  },
  {
    id: 'log-11',
    habitId: 'habit-4',
    date: '2026-09-29',
    completed: true,
  },
  {
    id: 'log-12',
    habitId: 'habit-4',
    date: '2026-09-30',
    completed: true,
  },
]