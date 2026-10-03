import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Lock, Mail } from 'lucide-react'

import { ApiError } from '../../api/client'
import { useAuth } from '../../auth/AuthContext'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'

interface LoginLocationState {
  from?: {
    pathname: string
  }
}

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async () => {
    setError('')

    if (!email.trim() || !password) {
      setError('Please enter your email and password.')
      return
    }

    setIsSubmitting(true)

    try {
      await login({
        email: email.trim(),
        password,
      })

      const state = location.state as LoginLocationState | null
      const destination = state?.from?.pathname ?? '/dashboard'

      navigate(destination, { replace: true })
    } catch (error) {
      if (error instanceof ApiError) {
        setError(error.message)
      } else {
        setError('Unable to login. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-slate-500">
          Welcome back
        </p>

        <h2 className="mt-1 text-2xl font-bold text-slate-800">
          Login to MindMirror
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Continue your personal reflection journey.
        </p>
      </div>

      <Card>
        <form
          className="space-y-5"
          onSubmit={(event) => {
            event.preventDefault()
            void handleSubmit()
          }}
        >
          <Input
            label="Email address"
            type="email"
            name="email"
            placeholder="you@example.com"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            disabled={isSubmitting}
          />

          <Input
            label="Password"
            type="password"
            name="password"
            placeholder="Enter your password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            disabled={isSubmitting}
          />

          {error && (
            <div
              className="rounded-lg border border-red-200 bg-red-50 p-3"
              role="alert"
            >
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          <Button
            type="submit"
            className="w-full"
            loading={isSubmitting}
          >
            <Lock className="mr-2 h-4 w-4" />
            Login
          </Button>
        </form>
      </Card>

      <p className="text-center text-sm text-slate-500">
        Don't have an account?{' '}
        <Link
          to="/signup"
          className="font-medium text-slate-700 underline decoration-slate-300 underline-offset-4 hover:text-slate-900"
        >
          Create an account
        </Link>
      </p>

      <div className="flex items-center justify-center gap-2 text-xs text-slate-400">
        <Mail className="h-3.5 w-3.5" />
        <span>
          Your personal data is protected by secure authentication.
        </span>
      </div>
    </div>
  )
}