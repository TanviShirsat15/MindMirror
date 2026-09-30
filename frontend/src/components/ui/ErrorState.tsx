import type { ReactNode } from 'react'

interface ErrorStateProps {
  title?: string
  message?: string
  action?: ReactNode
}

export default function ErrorState({
  title = 'Something went wrong',
  message = 'We could not load this content. Please try again.',
  action,
}: ErrorStateProps) {
  return (
    <div
      className="flex min-h-40 flex-col items-center justify-center rounded-xl border border-red-200 bg-red-50 p-6 text-center"
      role="alert"
    >
      <h3 className="text-sm font-semibold text-red-800">{title}</h3>

      <p className="mt-1 max-w-md text-sm text-red-700">
        {message}
      </p>

      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}