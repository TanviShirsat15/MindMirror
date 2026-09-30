import type { ReactNode } from 'react'

interface EmptyStateProps {
  title: string
  description?: string
  action?: ReactNode
}

export default function EmptyState({
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex min-h-40 flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
      <h3 className="text-sm font-semibold text-slate-700">{title}</h3>

      {description && (
        <p className="mt-1 max-w-md text-sm text-slate-500">
          {description}
        </p>
      )}

      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}