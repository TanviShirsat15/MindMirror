import { useState } from 'react'
import { BookOpen, CalendarDays, PenLine } from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import EmptyState from '../../components/ui/EmptyState'
import Input from '../../components/ui/Input'
import TextArea from '../../components/ui/TextArea'
import { journalEntries } from '../../mock/journalData'

export default function JournalPage() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')

  const handleSave = () => {
    if (!content.trim()) {
      return
    }

    setTitle('')
    setContent('')
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="border-b border-slate-200 pb-5">
        <p className="text-sm font-medium text-slate-500">
          Personal journal
        </p>

        <h1 className="mt-1 text-2xl font-bold text-slate-800">
          Journal
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Write freely about your thoughts, emotions, experiences, or
          anything you want to reflect on.
        </p>
      </div>

      {/* Composer */}
      <Card
        title="New journal entry"
        description="There is no word limit. Write as much or as little as you want."
      >
        <div className="space-y-4">
          <Input
            label="Title"
            placeholder="Give your entry a title"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />

          <TextArea
            label="Your reflection"
            placeholder="Start writing..."
            value={content}
            onChange={(event) => setContent(event.target.value)}
            rows={8}
          />

          <div className="flex justify-end">
            <Button
              onClick={handleSave}
              disabled={!content.trim()}
            >
              <PenLine className="mr-2 h-4 w-4" />
              Save Entry
            </Button>
          </div>
        </div>
      </Card>

      {/* Journal Timeline */}
      <Card
        title="Recent entries"
        description={`${journalEntries.length} entries shown in this demo`}
      >
        {journalEntries.length === 0 ? (
          <EmptyState
            title="No journal entries yet"
            description="Your saved reflections will appear here."
          />
        ) : (
          <div className="space-y-4">
            {journalEntries.map((entry) => (
              <article
                key={entry.id}
                className="rounded-xl border border-slate-200 p-4 transition hover:border-slate-300"
              >
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <h2 className="text-base font-semibold text-slate-800">
                      {entry.title}
                    </h2>

                    <div className="mt-1 flex items-center gap-2 text-xs text-slate-500">
                      <CalendarDays className="h-3.5 w-3.5" />

                      {new Date(entry.createdAt).toLocaleDateString(
                        'en-IN',
                        {
                          day: 'numeric',
                          month: 'short',
                          year: 'numeric',
                        },
                      )}
                    </div>
                  </div>

                  <Badge variant="info">
                    <BookOpen className="mr-1.5 h-3 w-3" />
                    Journal
                  </Badge>
                </div>

                <p className="mt-4 whitespace-pre-line text-sm leading-6 text-slate-600">
                  {entry.content}
                </p>
              </article>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}