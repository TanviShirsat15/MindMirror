import { Outlet, Link } from 'react-router-dom'

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 text-slate-800 antialiased">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link to="/dashboard" className="inline-flex items-center gap-2 mb-2 focus:outline-none focus:ring-2 focus:ring-teal-500 rounded-lg p-1">
          <div className="w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center font-bold text-base shadow-sm">
            MM
          </div>
          <span className="text-2xl font-bold text-slate-800 tracking-tight">MindMirror</span>
        </Link>
        <p className="text-xs text-slate-500 uppercase tracking-wider font-medium">
          Personal Well-Being & Habit Intelligence
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="bg-white py-8 px-6 shadow-sm border border-slate-200 rounded-2xl sm:px-10">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
