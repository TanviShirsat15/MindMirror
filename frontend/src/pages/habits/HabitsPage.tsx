import { useState } from 'react'
import { Check, Edit3, Plus, Target, Trash2 } from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import EmptyState from '../../components/ui/EmptyState'
import Input from '../../components/ui/Input'
import Modal from '../../components/ui/Modal'
import {
  habits as initialHabits,
  habitLogs as initialHabitLogs,
} from '../../mock/habitData'
import type { Habit, HabitLog } from '../../types/habit'

export default function HabitsPage() {
  const [habits, setHabits] = useState<Habit[]>(initialHabits)
  const [logs, setLogs] = useState<HabitLog[]>(initialHabitLogs)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingHabit, setEditingHabit] = useState<Habit | null>(null)
  const [name, setName] = useState('')
  const [targetPerWeek, setTargetPerWeek] = useState('3')
  const [savedMessage, setSavedMessage] = useState('')

  const openAddModal = () => {
    setEditingHabit(null)
    setName('')
    setTargetPerWeek('3')
    setIsModalOpen(true)
  }

  const openEditModal = (habit: Habit) => {
    setEditingHabit(habit)
    setName(habit.name)
    setTargetPerWeek(String(habit.targetPerWeek))
    setIsModalOpen(true)
  }

  const handleSaveHabit = () => {
    const trimmedName = name.trim()
    const target = Number(targetPerWeek)

    if (!trimmedName || target < 1 || target > 7) {
      return
    }

    if (editingHabit) {
      setHabits((currentHabits) =>
        currentHabits.map((habit) =>
          habit.id === editingHabit.id
            ? {
                ...habit,
                name: trimmedName,
                targetPerWeek: target,
              }
            : habit,
        ),
      )

      setSavedMessage('Habit updated')
    } else {
      const newHabit: Habit = {
        id: `demo-habit-${Date.now()}`,
        name: trimmedName,
        targetPerWeek: target,
        isActive: true,
        createdAt: new Date().toISOString(),
      }

      setHabits((currentHabits) => [...currentHabits, newHabit])
      setSavedMessage('Habit added')
    }

    setIsModalOpen(false)

    window.setTimeout(() => {
      setSavedMessage('')
    }, 2000)
  }

  const handleDeactivate = (habitId: string) => {
    setHabits((currentHabits) =>
      currentHabits.map((habit) =>
        habit.id === habitId
          ? { ...habit, isActive: false }
          : habit,
      ),
    )

    setSavedMessage('Habit deactivated')

    window.setTimeout(() => {
      setSavedMessage('')
    }, 2000)
  }

  const toggleCompletion = (habitId: string, date: string) => {
    setLogs((currentLogs) => {
      const existingLog = currentLogs.find(
        (log) => log.habitId === habitId && log.date === date,
      )

      if (existingLog) {
        return currentLogs.map((log) =>
          log.id === existingLog.id
            ? {
                ...log,
                completed: !log.completed,
              }
            : log,
        )
      }

      return [
        ...currentLogs,
        {
          id: `demo-log-${Date.now()}`,
          habitId,
          date,
          completed: true,
        },
      ]
    })
  }

  const activeHabits = habits.filter((habit) => habit.isActive)

  const completedCount = logs.filter(
    (log) => log.completed,
  ).length

  const trackedDays = new Set(
    logs.map((log) => log.date),
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
        {activeHabits.length === 0 ? (
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
              const habitLogs = logs.filter(
                (log) => log.habitId === habit.id,
              )

              const completed = habitLogs.filter(
                (log) => log.completed,
              ).length

              const completionRate =
                habitLogs.length > 0
                  ? Math.round(
                      (completed / habitLogs.length) * 100,
                    )
                  : 0

              const recentLogs = habitLogs.slice(-7)

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
                          Target: {habit.targetPerWeek} days per week
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
                        {completionRate}% recent completion
                      </Badge>

                      <Button
                        variant="ghost"
                        onClick={() => openEditModal(habit)}
                        aria-label={`Edit ${habit.name}`}
                      >
                        <Edit3 className="h-4 w-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        onClick={() => handleDeactivate(habit.id)}
                        aria-label={`Deactivate ${habit.name}`}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  {/* Completion Tracking */}
                  <div className="mt-4">
                    <p className="mb-2 text-xs font-medium text-slate-500">
                      Recent completion
                    </p>

                    <div className="grid grid-cols-7 gap-2">
                      {recentLogs.map((log) => (
                        <button
                          key={log.id}
                          type="button"
                          onClick={() =>
                            toggleCompletion(
                              habit.id,
                              log.date,
                            )
                          }
                          aria-label={`${log.completed ? 'Undo' : 'Mark'} ${habit.name} for ${log.date}`}
                          aria-pressed={log.completed}
                          className="flex flex-col items-center gap-1 rounded-lg p-1 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-300"
                        >
                          <span
                            className={`flex h-8 w-8 items-center justify-center rounded-full ${
                              log.completed
                                ? 'bg-emerald-50 text-emerald-700'
                                : 'bg-slate-100 text-slate-400'
                            }`}
                          >
                            {log.completed ? (
                              <Check className="h-4 w-4" />
                            ) : (
                              <span className="text-xs">
                                –
                              </span>
                            )}
                          </span>

                          <span className="text-[10px] text-slate-400">
                            {new Date(
                              log.date,
                            ).toLocaleDateString(
                              'en-IN',
                              {
                                day: 'numeric',
                              },
                            )}
                          </span>
                        </button>
                      ))}
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

      {/* Add/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
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
            label="Target per week"
            type="number"
            min="1"
            max="7"
            value={targetPerWeek}
            onChange={(event) =>
              setTargetPerWeek(event.target.value)
            }
            helperText="Choose how many days per week you want to target."
          />

          <div className="flex justify-end gap-2">
            <Button
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
            >
              Cancel
            </Button>

            <Button
              onClick={handleSaveHabit}
              disabled={!name.trim()}
            >
              {editingHabit ? 'Save Changes' : 'Add Habit'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}