import { useState } from 'react'
import {
  Bell,
  Check,
  Lock,
  User,
} from 'lucide-react'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'

export default function ProfileSettingsPage() {
  const [notifications, setNotifications] = useState(false)
  const [compactView, setCompactView] = useState(false)
  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    setSaved(true)

    window.setTimeout(() => {
      setSaved(false)
    }, 2000)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 pb-5">
        <p className="text-sm font-medium text-slate-500">
          Account preferences
        </p>

        <h1 className="mt-1 text-2xl font-bold text-slate-800">
          Profile & Settings
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Manage your profile information and application preferences.
        </p>
      </div>

      {/* Profile */}
      <Card
        title="Profile Information"
        description="Basic information for the current demo account."
      >
        <div className="grid gap-5 md:grid-cols-2">
          <Input
            label="Name"
            value="Demo User"
            readOnly
          />

          <Input
            label="Email"
            value="demo@mindmirror.local"
            readOnly
          />
        </div>
      </Card>

      {/* Preferences */}
      <Card
        title="Preferences"
        description="These controls currently demonstrate frontend behavior only."
      >
        <div className="space-y-4">
          <PreferenceRow
            icon={<Bell className="h-4 w-4" />}
            title="Enable notifications"
            description="Allow MindMirror to show notification reminders."
            checked={notifications}
            onChange={setNotifications}
          />

          <PreferenceRow
            icon={<User className="h-4 w-4" />}
            title="Use compact view"
            description="Use a more condensed presentation of interface content."
            checked={compactView}
            onChange={setCompactView}
          />
        </div>

        <div className="mt-5 flex items-center justify-end gap-3">
          {saved && (
            <Badge variant="success">
              <Check className="mr-1.5 h-3 w-3" />
              Saved
            </Badge>
          )}

          <Button onClick={handleSave}>
            Save Preferences
          </Button>
        </div>
      </Card>

      {/* Privacy */}
      <Card
        title="Privacy & Data"
        description="Important information about the current application stage."
      >
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <div className="flex items-start gap-3">
            <Lock className="mt-0.5 h-5 w-5 shrink-0 text-slate-500" />

            <div>
              <h3 className="text-sm font-semibold text-slate-800">
                Your journal data is intended to remain private
              </h3>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                Production authentication, authorization, secure
                persistence, and user-level data isolation will be
                implemented in later phases.
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* Demo Notice */}
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
        <p className="text-xs leading-5 text-slate-500">
          This Phase 3 screen uses frontend demo state only. Preferences
          are not persisted to the database yet.
        </p>
      </div>
    </div>
  )
}

interface PreferenceRowProps {
  icon: React.ReactNode
  title: string
  description: string
  checked: boolean
  onChange: (checked: boolean) => void
}

function PreferenceRow({
  icon,
  title,
  description,
  checked,
  onChange,
}: PreferenceRowProps) {
  return (
    <label className="flex cursor-pointer items-start justify-between gap-4 rounded-lg border border-slate-200 p-4 transition hover:border-slate-300">
      <div className="flex items-start gap-3">
        <div className="rounded-lg bg-slate-100 p-2 text-slate-600">
          {icon}
        </div>

        <div>
          <p className="text-sm font-medium text-slate-800">
            {title}
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            {description}
          </p>
        </div>
      </div>

      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
        className="mt-1 h-4 w-4 rounded border-slate-300 accent-slate-700 focus:ring-2 focus:ring-slate-300"
      />
    </label>
  )
}