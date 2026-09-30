import { Link, useNavigate } from 'react-router-dom'
import { Lock, UserPlus } from 'lucide-react'

import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'

export default function SignUpPage() {
  const navigate = useNavigate()

  const handleDemoSignup = () => {
    navigate('/dashboard')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-slate-500">
          Get started
        </p>

        <h2 className="mt-1 text-2xl font-bold text-slate-800">
          Create your MindMirror account
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Set up your personal space for journals, habits, and
          self-reflection.
        </p>
      </div>

      {/* Sign Up Form */}
      <Card>
        <div className="space-y-5">
          <Input
            label="Full name"
            type="text"
            placeholder="Your name"
            autoComplete="name"
          />

          <Input
            label="Email address"
            type="email"
            placeholder="you@example.com"
            autoComplete="email"
          />

          <Input
            label="Password"
            type="password"
            placeholder="Create a password"
            autoComplete="new-password"
          />

          <Button
            type="button"
            className="w-full"
            onClick={handleDemoSignup}
          >
            <UserPlus className="mr-2 h-4 w-4" />
            Create Demo Account
          </Button>

          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
            <p className="text-xs leading-5 text-slate-500">
              Demo mode: account creation, password hashing, and secure
              authentication will be implemented in later phases.
            </p>
          </div>
        </div>
      </Card>

      {/* Login */}
      <p className="text-center text-sm text-slate-500">
        Already have an account?{' '}
        <Link
          to="/login"
          className="font-medium text-slate-700 underline decoration-slate-300 underline-offset-4 hover:text-slate-900"
        >
          Sign in
        </Link>
      </p>

      {/* Security note */}
      <div className="flex items-center justify-center gap-2 text-xs text-slate-400">
        <Lock className="h-3.5 w-3.5" />
        <span>
          Secure authentication will be added in a later phase.
        </span>
      </div>
    </div>
  )
}