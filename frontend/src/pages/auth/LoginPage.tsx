import { Link } from 'react-router-dom'

export default function LoginPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Sign in to your account</h2>
        <p className="text-sm text-slate-500 mt-1">
          Or{' '}
          <Link to="/signup" className="text-teal-600 hover:text-teal-700 font-medium">
            create a new account
          </Link>
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="email">
            Email address
          </label>
          <input
            id="email"
            type="email"
            disabled
            placeholder="demo@mindmirror.local"
            className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            disabled
            placeholder="••••••••"
            className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-500"
          />
        </div>

        <Link
          to="/dashboard"
          className="w-full inline-flex justify-center items-center py-2.5 px-4 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-medium text-sm transition-colors"
        >
          Continue to Dashboard (Demo)
        </Link>
      </div>
    </div>
  )
}
