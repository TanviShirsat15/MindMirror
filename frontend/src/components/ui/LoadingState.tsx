import { Loader2 } from 'lucide-react'

interface LoadingStateProps {
  message?: string
}

export default function LoadingState({
  message = 'Loading...',
}: LoadingStateProps) {
  return (
    <div
      className="flex min-h-32 items-center justify-center rounded-xl border border-slate-200 bg-white p-6"
      role="status"
      aria-live="polite"
    >
      <div className="flex items-center gap-2 text-sm text-slate-500">
        <Loader2
          size={18}
          className="animate-spin"
          aria-hidden="true"
        />
        <span>{message}</span>
      </div>
    </div>
  )
}