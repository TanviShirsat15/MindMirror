import { Link } from 'react-router-dom'

export default function SignUpPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Create your account</h2>
        <p className="text-sm text-slate-500 mt-1">
          Already have an account?{' '}
          <Link to="/login" className="text-teal-600 hover:text-teal-700 font-medium">
            Sign in
          </Link>
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="signup-name">
            Full name
          </label>
          <input
            id="signup-name"
            type="text"
            disabled
            placeholder="Jane Doe"
            className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="signup-email">
            Email address
          </label>
          <input
            id="signup-email"
            type="email"
            disabled
            placeholder="jane@example.com"
            className="w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1" htmlFor="signup-password">
            Password
          </label>
          <input
            id="signup-password"
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
          Create Demo Account
        </Link>
      </div>
    </div>
  )
}
