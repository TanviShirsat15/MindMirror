import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Lock, UserPlus } from 'lucide-react'

import { ApiError } from '../../api/client'
import { useAuth } from '../../auth/AuthContext'
import Button from '../../components/ui/Button'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'

export default function SignUpPage() {
  const navigate = useNavigate()
  const { signup } = useAuth()

  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async () => {
    setError('')

    if (!fullName.trim()) {
      setError('Please enter your full name.')
      return
    }

    if (!email.trim()) {
      setError('Please enter your email address.')
      return
    }

    if (!password) {
      setError('Please enter a password.')
      return
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }

    setIsSubmitting(true)

    try {
      await signup({
        email: email.trim(),
        password,
        full_name: fullName.trim(),
      })

      navigate('/dashboard', { replace: true })
    } catch (error) {
      if (error instanceof ApiError) {
        setError(error.message)
      } else {
        setError('Unable to create your account. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
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

      {/* Signup Form */}
      <Card>
        <form
          className="space-y-5"
          onSubmit={(event) => {
            event.preventDefault()
            void handleSubmit()
          }}
        >
          <Input
            label="Full name"
            type="text"
            name="fullName"
            placeholder="Your name"
            autoComplete="name"
            value={fullName}
            onChange={(event) => setFullName(event.target.value)}
            disabled={isSubmitting}
          />

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
            placeholder="Create a password"
            autoComplete="new-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            disabled={isSubmitting}
            helperText="Password must be at least 8 characters long."
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
            <UserPlus className="mr-2 h-4 w-4" />
            Create Account
          </Button>
        </form>
      </Card>

      {/* Login Link */}
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
          Your password is securely protected.
        </span>
      </div>
    </div>
  )
}