import type { JournalEntry } from '../types/journal'

export const journalEntries: JournalEntry[] = [
  {
    id: 'journal-1',
    title: 'A productive day',
    content:
      'Today I completed most of my planned tasks and felt focused during the afternoon. I also went for a short walk and had some time to relax.',
    createdAt: '2026-09-28T18:30:00',
  },
  {
    id: 'journal-2',
    title: 'Feeling a little tired',
    content:
      'I had a busy day and did not sleep very well last night. I managed to finish my important work, but I felt tired by the evening.',
    createdAt: '2026-09-29T20:15:00',
  },
  {
    id: 'journal-3',
    title: 'Good progress',
    content:
      'Today felt balanced. I studied for a few hours, completed my exercise goal, and spent some time reading. I feel satisfied with the progress I made.',
    createdAt: '2026-09-30T19:45:00',
  },
]