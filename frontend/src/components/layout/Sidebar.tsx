import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  BookOpen,
  CheckSquare,
  Sparkles,
  LineChart,
  Lightbulb,
  Settings,
  X,
} from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const navItems = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Journal', path: '/journal', icon: BookOpen },
  { name: 'Habits', path: '/habits', icon: CheckSquare },
  { name: 'Well-Being Analysis', path: '/wellbeing', icon: Sparkles },
  { name: 'Analytics / History', path: '/analytics', icon: LineChart },
  { name: 'Insights', path: '/insights', icon: Lightbulb },
  { name: 'Settings', path: '/settings', icon: Settings },
]

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-slate-900/30 backdrop-blur-sm lg:hidden transition-opacity"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar drawer */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 w-64 bg-white border-r border-slate-200 transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:z-10 flex flex-col ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        aria-label="Sidebar navigation"
      >
        {/* Mobile header with close button */}
        <div className="flex items-center justify-between p-4 border-b border-slate-200 lg:hidden">
          <span className="font-bold text-slate-800">MindMirror Navigation</span>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
            aria-label="Close navigation menu"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation links */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-teal-50 text-teal-700 font-semibold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                  }`
                }
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            )
          })}
        </nav>

        {/* Auth demonstration links (Phase 3 UI shell) */}
        <div className="p-3 border-t border-slate-100 space-y-1">
          <div className="px-3 py-1 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Auth Demos
          </div>
          <NavLink
            to="/login"
            className="flex items-center gap-2 px-3 py-1.5 text-xs text-slate-500 hover:text-slate-700 hover:bg-slate-50 rounded"
          >
            <span>View Login Page</span>
          </NavLink>
          <NavLink
            to="/signup"
            className="flex items-center gap-2 px-3 py-1.5 text-xs text-slate-500 hover:text-slate-700 hover:bg-slate-50 rounded"
          >
            <span>View Sign Up Page</span>
          </NavLink>
        </div>
      </aside>
    </>
  )
}
