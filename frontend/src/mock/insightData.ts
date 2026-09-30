import type { Insight } from '../types/insight'

export const insights: Insight[] = [
  {
    id: 'insight-1',
    category: 'baseline',
    title: 'Above your recent baseline',
    description:
      'Your latest well-being score is above your current personal baseline.',
    createdAt: '2026-09-30T20:00:00',
  },
  {
    id: 'insight-2',
    category: 'trend',
    title: 'Recent upward trend',
    description:
      'Your well-being scores have generally increased across the last few entries.',
    createdAt: '2026-09-30T20:05:00',
  },
  {
    id: 'insight-3',
    category: 'habit',
    title: 'Higher scores with stronger habit consistency',
    description:
      'Recent entries with higher habit consistency have also shown higher well-being scores.',
    createdAt: '2026-09-30T20:10:00',
  },
  {
    id: 'insight-4',
    category: 'emotional',
    title: 'Positive sentiment has increased',
    description:
      'Your recent journal-related sentiment signal is higher than it was earlier in the displayed period.',
    createdAt: '2026-09-30T20:15:00',
  },
  {
    id: 'insight-5',
    category: 'consistency',
    title: 'Habit consistency is improving',
    description:
      'Your recent habit completion pattern shows stronger consistency compared with the beginning of the displayed period.',
    createdAt: '2026-09-30T20:20:00',
  },
  {
    id: 'insight-6',
    category: 'recent-change',
    title: 'Recent change detected',
    description:
      'Your latest score is higher than the score recorded two days earlier.',
    createdAt: '2026-09-30T20:25:00',
  },
]