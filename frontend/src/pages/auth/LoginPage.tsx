import { Link, useNavigate } from 'react-router-dom'
import { Lock, Mail } from 'lucide-react'

import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'

export default function LoginPage() {
  const navigate = useNavigate()

  const handleDemoLogin = () => {
    navigate('/dashboard')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-slate-500">
          Welcome back
        </p>

        <h2 className="mt-1 text-2xl font-bold text-slate-800">
          Sign in to MindMirror
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Continue your personal reflection journey.
        </p>
      </div>

      {/* Login Form */}
      <Card>
        <div className="space-y-5">
          <Input
            label="Email address"
            type="email"
            placeholder="you@example.com"
            autoComplete="email"
          />

          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            autoComplete="current-password"
          />

          <Button
            type="button"
            className="w-full"
            onClick={handleDemoLogin}
          >
            <Lock className="mr-2 h-4 w-4" />
            Continue to Dashboard
          </Button>

          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
            <p className="text-xs leading-5 text-slate-500">
              Demo mode: authentication will be implemented in a later
              phase. This button currently opens the dashboard.
            </p>
          </div>
        </div>
      </Card>

      {/* Sign Up */}
      <p className="text-center text-sm text-slate-500">
        Don't have an account?{' '}
        <Link
          to="/signup"
          className="font-medium text-slate-700 underline decoration-slate-300 underline-offset-4 hover:text-slate-900"
        >
          Create an account
        </Link>
      </p>

      {/* Privacy note */}
      <div className="flex items-center justify-center gap-2 text-xs text-slate-400">
        <Mail className="h-3.5 w-3.5" />
        <span>Your personal data will be protected in later security phases.</span>
      </div>
    </div>
  )
}