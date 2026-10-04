import { useEffect, useMemo, useState } from 'react'
import { Check, Edit3, Plus, Target, Trash2 } from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import EmptyState from '../../components/ui/EmptyState'
import Input from '../../components/ui/Input'
import Modal from '../../components/ui/Modal'
import {
  ApiError,
  apiDelete,
  apiGet,
  apiPost,
  apiPut,
} from '../../api/client'
import type { Habit, HabitLog, HabitMetrics } from '../../types/habit'

interface HabitWithData extends Habit {
  logs: HabitLog[]
  metrics: HabitMetrics | null
}


function getRecentDates(): string[] {
  const today = new Date()
  const dates: string[] = []

  for (let index = 6; index >= 0; index -= 1) {
    const date = new Date(today)
    date.setDate(today.getDate() - index)

    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')

    dates.push(`${year}-${month}-${day}`)
  }

  return dates
}

function formatDateLabel(dateValue: string): string {
  const date = new Date(`${dateValue}T00:00:00`)

  return date.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
  })
}

function formatTarget(habit: Habit): string {
  const unit = habit.target_unit?.trim()

  if (!unit) {
    return String(habit.target_value)
  }

  return `${habit.target_value} ${unit}`
}

export default function HabitsPage() {
  const [habits, setHabits] = useState<HabitWithData[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')
  const [savedMessage, setSavedMessage] = useState('')

  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)

  const [editingHabit, setEditingHabit] = useState<Habit | null>(null)
  const [deletingHabit, setDeletingHabit] = useState<Habit | null>(null)

  const [name, setName] = useState('')
  const [targetValue, setTargetValue] = useState('1')
  const [targetUnit, setTargetUnit] = useState('')

  const [isSaving, setIsSaving] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [updatingHabitId, setUpdatingHabitId] = useState<number | null>(null)

  const recentDates = useMemo(() => getRecentDates(), [])

  const showSavedMessage = (message: string) => {
    setSavedMessage(message)

    window.setTimeout(() => {
      setSavedMessage('')
    }, 2000)
  }

  const loadHabits = async () => {
    setIsLoading(true)
    setErrorMessage('')

    try {
      const habitList = await apiGet<Habit[]>('/api/habits')

      const habitData = await Promise.all(
        habitList.map(async (habit) => {
          const [logs, metrics] = await Promise.all([
            apiGet<HabitLog[]>(
              `/api/habit-logs/${habit.id}?start_date=${recentDates[0]}&end_date=${recentDates[6]}`,
            ),
            apiGet<HabitMetrics>(
              `/api/habits/${habit.id}/metrics?window=weekly`,
            ),
          ])

          return {
            ...habit,
            logs,
            metrics,
          }
        }),
      )

      setHabits(habitData)
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage('Unable to load habits. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    void loadHabits()
  }, [])

  const openAddModal = () => {
    setEditingHabit(null)
    setName('')
    setTargetValue('1')
    setTargetUnit('')
    setErrorMessage('')
    setIsModalOpen(true)
  }

  const openEditModal = (habit: Habit) => {
    setEditingHabit(habit)
    setName(habit.name)
    setTargetValue(String(habit.target_value))
    setTargetUnit(habit.target_unit ?? '')
    setErrorMessage('')
    setIsModalOpen(true)
  }

  const closeHabitModal = () => {
    if (isSaving) {
      return
    }

    setIsModalOpen(false)
    setEditingHabit(null)
    setName('')
    setTargetValue('1')
    setTargetUnit('')
  }

  const handleSaveHabit = async () => {
    const trimmedName = name.trim()
    const numericTarget = Number(targetValue)

    if (!trimmedName) {
      setErrorMessage('Habit name cannot be empty.')
      return
    }

    if (!Number.isFinite(numericTarget) || numericTarget <= 0) {
      setErrorMessage('Habit target must be greater than zero.')
      return
    }

    setIsSaving(true)
    setErrorMessage('')

    try {
      if (editingHabit) {
        await apiPut<Habit>(`/api/habits/${editingHabit.id}`, {
          name: trimmedName,
          target_value: numericTarget,
          target_unit: targetUnit.trim() || null,
          frequency: 'daily',
        })

        showSavedMessage('Habit updated')
      } else {
        await apiPost<Habit>('/api/habits', {
          name: trimmedName,
          target_value: numericTarget,
          target_unit: targetUnit.trim() || null,
          frequency: 'daily',
        })

        showSavedMessage('Habit added')
      }

      closeHabitModal()
      await loadHabits()
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage('Unable to save habit. Please try again.')
      }
    } finally {
      setIsSaving(false)
    }
  }

  const handleDeactivate = async (habit: Habit) => {
    setUpdatingHabitId(habit.id)
    setErrorMessage('')

    try {
      await apiPut<Habit>(`/api/habits/${habit.id}`, {
        is_active: false,
      })

      showSavedMessage('Habit deactivated')
      await loadHabits()
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage('Unable to deactivate habit. Please try again.')
      }
    } finally {
      setUpdatingHabitId(null)
    }
  }

  const handleReactivate = async (habit: Habit) => {
    setUpdatingHabitId(habit.id)
    setErrorMessage('')

    try {
      await apiPut<Habit>(`/api/habits/${habit.id}`, {
        is_active: true,
      })

      showSavedMessage('Habit reactivated')
      await loadHabits()
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage('Unable to reactivate habit. Please try again.')
      }
    } finally {
      setUpdatingHabitId(null)
    }
  }

  const openDeleteModal = (habit: Habit) => {
    setDeletingHabit(habit)
    setErrorMessage('')
    setIsDeleteModalOpen(true)
  }

  const closeDeleteModal = () => {
    if (isDeleting) {
      return
    }

    setIsDeleteModalOpen(false)
    setDeletingHabit(null)
  }

  const handleHardDelete = async () => {
    if (!deletingHabit) {
      return
    }

    setIsDeleting(true)
    setErrorMessage('')

    try {
      await apiDelete<void>(`/api/habits/${deletingHabit.id}`)

      showSavedMessage('Habit permanently deleted')
      closeDeleteModal()
      await loadHabits()
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage('Unable to delete habit. Please try again.')
      }
    } finally {
      setIsDeleting(false)
    }
  }

  const toggleCompletion = async (
    habit: Habit,
    date: string,
    isCompleted: boolean,
  ) => {
    setUpdatingHabitId(habit.id)
    setErrorMessage('')

    try {
      if (isCompleted) {
        await apiPost<HabitLog>(
          `/api/habits/${habit.id}/undo?log_date=${date}`,
          {},
        )
      } else {
        await apiPost<HabitLog>(
          `/api/habits/${habit.id}/complete?log_date=${date}`,
          {},
        )
      }

      await loadHabits()
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage(
          'Unable to update completion. Please try again.',
        )
      }
    } finally {
      setUpdatingHabitId(null)
    }
  }

  const activeHabits = habits.filter((habit) => habit.is_active)
  const inactiveHabits = habits.filter((habit) => !habit.is_active)

  const completedCount = habits.reduce(
    (total, habit) =>
      total +
      habit.logs.filter((log) => log.is_completed).length,
    0,
  )

  const trackedDays = new Set(
    habits.flatMap((habit) => habit.logs.map((log) => log.log_date)),
  ).size

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col gap-4 border-b border-slate-200 pb-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Behavioral routines
          </p>

          <h1 className="mt-1 text-2xl font-bold text-slate-800">
            Habits
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Create and track routines that are meaningful to you.
          </p>
        </div>

        <Button onClick={openAddModal}>
          <Plus className="mr-2 h-4 w-4" />
          Add Habit
        </Button>
      </div>

      {/* Feedback */}
      {savedMessage && (
        <div
          role="status"
          className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600"
        >
          {savedMessage}
        </div>
      )}

      {errorMessage && (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          {errorMessage}
        </div>
      )}

      {/* Habit Summary */}
      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <p className="text-sm text-slate-500">
            Active habits
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-800">
            {activeHabits.length}
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Recent completions
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-800">
            {completedCount}
          </p>
        </Card>

        <Card>
          <p className="text-sm text-slate-500">
            Tracked days
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-800">
            {trackedDays}
          </p>
        </Card>
      </div>

      {/* Habits */}
      <Card
        title="Your habits"
        description="Targets and recent completion activity."
      >
        {isLoading ? (
          <div className="py-10 text-center text-sm text-slate-500">
            Loading habits...
          </div>
        ) : activeHabits.length === 0 ? (
          <EmptyState
            title="No active habits"
            description="Add a habit to start tracking your routine."
            action={
              <Button onClick={openAddModal}>
                <Plus className="mr-2 h-4 w-4" />
                Add Habit
              </Button>
            }
          />
        ) : (
          <div className="space-y-4">
            {activeHabits.map((habit) => {
              const logByDate = new Map(
                habit.logs.map((log) => [log.log_date, log]),
              )

              const completionRate =
                habit.metrics?.completion_rate ?? 0

              const currentStreak =
                habit.metrics?.current_streak ?? 0

              const longestStreak =
                habit.metrics?.longest_streak ?? 0

              const isUpdating = updatingHabitId === habit.id

              return (
                <div
                  key={habit.id}
                  className="rounded-xl border border-slate-200 p-4"
                >
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-start gap-3">
                      <div className="rounded-lg bg-slate-100 p-2.5">
                        <Target className="h-5 w-5 text-slate-600" />
                      </div>

                      <div>
                        <h2 className="text-sm font-semibold text-slate-800">
                          {habit.name}
                        </h2>

                        <p className="mt-1 text-xs text-slate-500">
                          Target: {formatTarget(habit)} daily
                        </p>
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      <Badge
                        variant={
                          completionRate >= 70
                            ? 'success'
                            : completionRate >= 40
                              ? 'warning'
                              : 'default'
                        }
                      >
                        {completionRate}% weekly completion
                      </Badge>

                      <Button
                        variant="ghost"
                        onClick={() => openEditModal(habit)}
                        disabled={isUpdating}
                        aria-label={`Edit ${habit.name}`}
                      >
                        <Edit3 className="h-4 w-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        onClick={() => handleDeactivate(habit)}
                        disabled={isUpdating}
                        aria-label={`Deactivate ${habit.name}`}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  {/* Metrics */}
                  <div className="mt-4 grid gap-3 sm:grid-cols-3">
                    <div className="rounded-lg bg-slate-50 px-3 py-2">
                      <p className="text-xs text-slate-500">
                        Weekly completion
                      </p>
                      <p className="mt-1 text-sm font-semibold text-slate-700">
                        {habit.metrics?.completed_days ?? 0}/
                        {habit.metrics?.expected_days ?? 7} days
                      </p>
                    </div>

                    <div className="rounded-lg bg-slate-50 px-3 py-2">
                      <p className="text-xs text-slate-500">
                        Current streak
                      </p>
                      <p className="mt-1 text-sm font-semibold text-slate-700">
                        {currentStreak} day
                        {currentStreak === 1 ? '' : 's'}
                      </p>
                    </div>

                    <div className="rounded-lg bg-slate-50 px-3 py-2">
                      <p className="text-xs text-slate-500">
                        Longest streak
                      </p>
                      <p className="mt-1 text-sm font-semibold text-slate-700">
                        {longestStreak} day
                        {longestStreak === 1 ? '' : 's'}
                      </p>
                    </div>
                  </div>

                  {/* Completion Tracking */}
                  <div className="mt-4">
                    <p className="mb-2 text-xs font-medium text-slate-500">
                      Last 7 days
                    </p>

                    <div className="grid grid-cols-7 gap-2">
                      {recentDates.map((date) => {
                        const log = logByDate.get(date)
                        const completed = log?.is_completed ?? false

                        return (
                          <button
                            key={date}
                            type="button"
                            disabled={isUpdating}
                            onClick={() =>
                              toggleCompletion(
                                habit,
                                date,
                                completed,
                              )
                            }
                            aria-label={`${
                              completed ? 'Undo' : 'Mark'
                            } ${habit.name} for ${date}`}
                            aria-pressed={completed}
                            className="flex flex-col items-center gap-1 rounded-lg p-1 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-300 disabled:cursor-not-allowed disabled:opacity-50"
                          >
                            <span
                              className={`flex h-8 w-8 items-center justify-center rounded-full ${
                                completed
                                  ? 'bg-emerald-50 text-emerald-700'
                                  : 'bg-slate-100 text-slate-400'
                              }`}
                            >
                              {completed ? (
                                <Check className="h-4 w-4" />
                              ) : (
                                <span className="text-xs">–</span>
                              )}
                            </span>

                            <span className="text-[10px] text-slate-400">
                              {formatDateLabel(date)}
                            </span>
                          </button>
                        )
                      })}
                    </div>

                    <p className="mt-2 text-xs text-slate-400">
                      Click a day to mark it complete or undo the
                      completion.
                    </p>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </Card>

      {/* Inactive Habits */}
      {!isLoading && inactiveHabits.length > 0 && (
        <Card
          title="Inactive habits"
          description="Deactivated habits remain available so their history is preserved."
        >
          <div className="space-y-3">
            {inactiveHabits.map((habit) => (
              <div
                key={habit.id}
                className="flex flex-col gap-3 rounded-xl border border-slate-200 p-4 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <h2 className="text-sm font-semibold text-slate-700">
                    {habit.name}
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    Target: {formatTarget(habit)} daily
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => handleReactivate(habit)}
                    disabled={updatingHabitId === habit.id}
                  >
                    Reactivate
                  </Button>

                  <Button
                    variant="ghost"
                    onClick={() => openDeleteModal(habit)}
                    disabled={updatingHabitId === habit.id}
                    aria-label={`Permanently delete ${habit.name}`}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Add/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={closeHabitModal}
        title={editingHabit ? 'Edit Habit' : 'Add Habit'}
      >
        <div className="space-y-4">
          <Input
            label="Habit name"
            placeholder="e.g. Exercise"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />

          <Input
            label="Daily target"
            type="number"
            min="0.01"
            step="0.01"
            value={targetValue}
            onChange={(event) =>
              setTargetValue(event.target.value)
            }
            helperText="Enter the amount you want to complete each day."
          />

          <Input
            label="Target unit"
            placeholder="e.g. minutes, glasses, pages"
            value={targetUnit}
            onChange={(event) =>
              setTargetUnit(event.target.value)
            }
            helperText="Optional. Use a unit that makes sense for your habit."
          />

          <div className="rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500">
            Frequency: Daily
          </div>

          <div className="flex justify-end gap-2">
            <Button
              variant="secondary"
              onClick={closeHabitModal}
              disabled={isSaving}
            >
              Cancel
            </Button>

            <Button
              onClick={handleSaveHabit}
              disabled={!name.trim() || isSaving}
            >
              {isSaving
                ? 'Saving...'
                : editingHabit
                  ? 'Save Changes'
                  : 'Add Habit'}
            </Button>
          </div>
        </div>
      </Modal>

      {/* Hard Delete Confirmation */}
      <Modal
        isOpen={isDeleteModalOpen}
        onClose={closeDeleteModal}
        title="Permanently Delete Habit"
      >
        <div className="space-y-4">
          <p className="text-sm leading-6 text-slate-600">
            Are you sure you want to permanently delete{' '}
            <span className="font-semibold text-slate-800">
              {deletingHabit?.name}
            </span>
            ?
          </p>

          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            This action is irreversible and will also delete the
            habit's completion history.
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
              onClick={handleHardDelete}
              disabled={isDeleting}
            >
              {isDeleting ? 'Deleting...' : 'Delete Permanently'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}