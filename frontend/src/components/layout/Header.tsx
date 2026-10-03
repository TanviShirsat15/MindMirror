import { LogOut, Menu, User } from 'lucide-react'

import { useAuth } from '../../auth/AuthContext'

interface HeaderProps {
  onToggleSidebar: () => void
}

export default function Header({ onToggleSidebar }: HeaderProps) {
  const { user, logout } = useAuth()

  const displayName = user?.full_name || 'MindMirror User'

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onToggleSidebar}
          className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-700 focus:outline-none focus:ring-2 focus:ring-teal-500 lg:hidden"
          aria-label="Toggle navigation menu"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-sm font-bold tracking-wider text-white shadow-sm">
            MM
          </div>

          <span className="text-lg font-bold tracking-tight text-slate-800">
            MindMirror
          </span>
        </div>
      </div>

      {/* Authenticated user */}
      <div className="flex items-center gap-3">
        <div className="hidden text-right sm:flex sm:flex-col">
          <span className="text-sm font-medium text-slate-700">
            {displayName}
          </span>

          <span className="text-xs text-slate-400">
            {user?.email}
          </span>
        </div>

        <div
          className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-slate-100 text-slate-600"
          aria-label="User profile avatar"
        >
          <User className="h-4 w-4" />
        </div>

        <button
          type="button"
          onClick={logout}
          className="rounded-lg p-2 text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
          aria-label="Log out"
          title="Log out"
        >
          <LogOut className="h-4 w-4" />
        </button>
      </div>
    </header>
  )
}