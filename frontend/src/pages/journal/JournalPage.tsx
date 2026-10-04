import { useEffect, useMemo, useState } from 'react'
import {
  BookOpen,
  CalendarDays,
  Check,
  Pencil,
  PenLine,
  Trash2,
} from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import EmptyState from '../../components/ui/EmptyState'
import Modal from '../../components/ui/Modal'
import TextArea from '../../components/ui/TextArea'
import {
  apiDelete,
  apiGet,
  apiPost,
  apiPut,
  ApiError,
} from '../../api/client'

interface JournalEntry {
  id: number
  user_id: number
  content: string
  entry_date: string
  created_at: string
  updated_at: string
}

function getTodayDate(): string {
  const today = new Date()

  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function formatDate(dateString: string): string {
  const [year, month, day] = dateString.split('-').map(Number)

  if (!year || !month || !day) {
    return dateString
  }

  return new Date(year, month - 1, day).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

function sortJournalEntries(entries: JournalEntry[]): JournalEntry[] {
  return [...entries].sort((a, b) => {
    const dateDifference =
      new Date(`${b.entry_date}T00:00:00`).getTime() -
      new Date(`${a.entry_date}T00:00:00`).getTime()

    if (dateDifference !== 0) {
      return dateDifference
    }

    return (
      new Date(b.created_at).getTime() -
      new Date(a.created_at).getTime()
    )
  })
}

export default function JournalPage() {
  const [content, setContent] = useState('')
  const [entryDate, setEntryDate] = useState(getTodayDate())

  const [entries, setEntries] = useState<JournalEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [savedMessage, setSavedMessage] = useState('')

  const [editingEntry, setEditingEntry] = useState<JournalEntry | null>(null)
  const [editContent, setEditContent] = useState('')
  const [editDate, setEditDate] = useState('')
  const [isUpdating, setIsUpdating] = useState(false)

  const [deletingEntry, setDeletingEntry] = useState<JournalEntry | null>(
    null,
  )
  const [isDeleting, setIsDeleting] = useState(false)

  const sortedEntries = useMemo(
    () => sortJournalEntries(entries),
    [entries],
  )

  const loadEntries = async () => {
    setIsLoading(true)
    setError('')

    try {
      const data = await apiGet<JournalEntry[]>('/api/journals')
      setEntries(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Unable to load journal entries.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    void loadEntries()
  }, [])

  const handleSave = async () => {
    if (!content.trim()) {
      setError('Journal content cannot be empty.')
      return
    }

    setIsSaving(true)
    setError('')
    setSavedMessage('')

    try {
      const newEntry = await apiPost<JournalEntry>('/api/journals', {
        content,
        entry_date: entryDate,
      })

      setEntries((currentEntries) => [
        newEntry,
        ...currentEntries,
      ])

      setContent('')
      setEntryDate(getTodayDate())
      setSavedMessage('Journal entry saved.')

      window.setTimeout(() => {
        setSavedMessage('')
      }, 2000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Unable to save journal entry.')
      }
    } finally {
      setIsSaving(false)
    }
  }

  const openEditModal = (entry: JournalEntry) => {
    setEditingEntry(entry)
    setEditContent(entry.content)
    setEditDate(entry.entry_date)
    setError('')
  }

  const closeEditModal = () => {
    if (isUpdating) {
      return
    }

    setEditingEntry(null)
    setEditContent('')
    setEditDate('')
  }

  const handleUpdate = async () => {
    if (!editingEntry) {
      return
    }

    if (!editContent.trim()) {
      setError('Journal content cannot be empty.')
      return
    }

    setIsUpdating(true)
    setError('')

    try {
      const updatedEntry = await apiPut<JournalEntry>(
        `/api/journals/${editingEntry.id}`,
        {
          content: editContent,
          entry_date: editDate,
        },
      )

      setEntries((currentEntries) =>
        currentEntries.map((entry) =>
          entry.id === updatedEntry.id ? updatedEntry : entry,
        ),
      )

      closeEditModal()
      setSavedMessage('Journal entry updated.')

      window.setTimeout(() => {
        setSavedMessage('')
      }, 2000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Unable to update journal entry.')
      }
    } finally {
      setIsUpdating(false)
    }
  }

  const openDeleteModal = (entry: JournalEntry) => {
    setDeletingEntry(entry)
    setError('')
  }

  const closeDeleteModal = () => {
    if (isDeleting) {
      return
    }

    setDeletingEntry(null)
  }

  const handleDelete = async () => {
    if (!deletingEntry) {
      return
    }

    setIsDeleting(true)
    setError('')

    try {
      await apiDelete(`/api/journals/${deletingEntry.id}`)

      setEntries((currentEntries) =>
        currentEntries.filter(
          (entry) => entry.id !== deletingEntry.id,
        ),
      )

      closeDeleteModal()
      setSavedMessage('Journal entry deleted.')

      window.setTimeout(() => {
        setSavedMessage('')
      }, 2000)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Unable to delete journal entry.')
      }
    } finally {
      setIsDeleting(false)
    }
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

      {/* Success Feedback */}
      {savedMessage && (
        <div
          role="status"
          className="flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600"
        >
          <Check className="h-4 w-4 text-slate-500" />
          {savedMessage}
        </div>
      )}

      {/* Error Feedback */}
      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          {error}
        </div>
      )}

      {/* Composer */}
      <Card
        title="New journal entry"
        description="There is no word limit. Write as much or as little as you want."
      >
        <div className="space-y-4">
          <div>
            <label
              htmlFor="journal-entry-date"
              className="mb-1.5 block text-sm font-medium text-slate-700"
            >
              Date
            </label>

            <input
              id="journal-entry-date"
              type="date"
              value={entryDate}
              onChange={(event) => setEntryDate(event.target.value)}
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            />
          </div>

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
              disabled={!content.trim() || isSaving}
            >
              <PenLine className="mr-2 h-4 w-4" />

              {isSaving ? 'Saving...' : 'Save Entry'}
            </Button>
          </div>
        </div>
      </Card>

      {/* Journal History */}
      <Card
        title="Recent entries"
        description={
          sortedEntries.length === 0
            ? 'Your saved reflections will appear here.'
            : `${sortedEntries.length} ${
                sortedEntries.length === 1 ? 'entry' : 'entries'
              }`
        }
      >
        {isLoading ? (
          <div
            className="py-10 text-center text-sm text-slate-500"
            role="status"
          >
            Loading journal entries...
          </div>
        ) : sortedEntries.length === 0 ? (
          <EmptyState
            title="No journal entries yet"
            description="Your saved reflections will appear here."
          />
        ) : (
          <div className="space-y-4">
            {sortedEntries.map((entry) => (
              <article
                key={entry.id}
                className="rounded-xl border border-slate-200 p-4 transition hover:border-slate-300"
              >
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <CalendarDays className="h-4 w-4 text-slate-500" />

                      <p className="text-sm font-medium text-slate-700">
                        {formatDate(entry.entry_date)}
                      </p>
                    </div>

                    <p className="mt-1 text-xs text-slate-400">
                      Saved{' '}
                      {new Date(entry.created_at).toLocaleString(
                        'en-IN',
                      )}
                    </p>
                  </div>

                  <Badge variant="info">
                    <BookOpen className="mr-1.5 h-3 w-3" />
                    Journal
                  </Badge>
                </div>

                <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-slate-600">
                  {entry.content}
                </p>

                <div className="mt-4 flex flex-wrap justify-end gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => openEditModal(entry)}
                  >
                    <Pencil className="mr-2 h-4 w-4" />
                    Edit
                  </Button>

                  <Button
                    variant="secondary"
                    onClick={() => openDeleteModal(entry)}
                  >
                    <Trash2 className="mr-2 h-4 w-4" />
                    Delete
                  </Button>
                </div>
              </article>
            ))}
          </div>
        )}
      </Card>

      {/* Edit Modal */}
      <Modal
        isOpen={editingEntry !== null}
        onClose={closeEditModal}
        title="Edit journal entry"
      >
        <div className="space-y-4">
          <div>
            <label
              htmlFor="edit-journal-date"
              className="mb-1.5 block text-sm font-medium text-slate-700"
            >
              Date
            </label>

            <input
              id="edit-journal-date"
              type="date"
              value={editDate}
              onChange={(event) => setEditDate(event.target.value)}
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
              disabled={isUpdating}
            />
          </div>

          <TextArea
            label="Your reflection"
            value={editContent}
            onChange={(event) => setEditContent(event.target.value)}
            rows={10}
          />

          <div className="flex justify-end gap-2">
            <Button
              variant="secondary"
              onClick={closeEditModal}
              disabled={isUpdating}
            >
              Cancel
            </Button>

            <Button
              onClick={handleUpdate}
              disabled={!editContent.trim() || isUpdating}
            >
              {isUpdating ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </div>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={deletingEntry !== null}
        onClose={closeDeleteModal}
        title="Delete journal entry"
      >
        <div className="space-y-5">
          <p className="text-sm leading-6 text-slate-600">
            Are you sure you want to delete this journal entry?
            This action cannot be undone.
          </p>

          <div className="rounded-lg bg-slate-50 p-3">
            <p className="line-clamp-4 whitespace-pre-wrap text-sm text-slate-600">
              {deletingEntry?.content}
            </p>
          </div>

          <div className="flex justify-end gap-2">
            <Button
              variant="secondary"
              onClick={closeDeleteModal}
              disabled={isDeleting}
            >
              Cancel
            </Button>

            <Button
              onClick={handleDelete}
              disabled={isDeleting}
            >
              {isDeleting ? 'Deleting...' : 'Delete Entry'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}