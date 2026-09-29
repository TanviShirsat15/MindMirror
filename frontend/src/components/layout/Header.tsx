import { Menu, User } from 'lucide-react'

interface HeaderProps {
  onToggleSidebar: () => void
}

export default function Header({ onToggleSidebar }: HeaderProps) {
  return (
    <header className="sticky top-0 z-20 bg-white border-b border-slate-200 h-16 flex items-center justify-between px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onToggleSidebar}
          className="lg:hidden p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
          aria-label="Toggle navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-teal-600 text-white flex items-center justify-center font-bold text-sm tracking-wider shadow-sm">
            MM
          </div>
          <span className="text-lg font-bold text-slate-800 tracking-tight">MindMirror</span>
        </div>
      </div>

      {/* Placeholder user profile menu (mock data, no real account) */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex flex-col text-right">
          <span className="text-sm font-medium text-slate-700">Demo User</span>
          <span className="text-xs text-slate-400">demo@mindmirror.local</span>
        </div>
        <div
          className="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600"
          aria-label="User profile avatar"
        >
          <User className="w-4 h-4" />
        </div>
      </div>
    </header>
  )
}
