import type { ReactNode } from 'react'

interface ChartContainerProps {
  title?: string
  description?: string
  children: ReactNode
  className?: string
}

export default function ChartContainer({
  title,
  description,
  children,
  className = '',
}: ChartContainerProps) {
  return (
    <section
      className={`rounded-xl border border-slate-200 bg-white p-5 shadow-sm ${className}`}
    >
      {(title || description) && (
        <div className="mb-4">
          {title && (
            <h2 className="text-base font-semibold text-slate-800">
              {title}
            </h2>
          )}

          {description && (
            <p className="mt-1 text-sm text-slate-500">
              {description}
            </p>
          )}
        </div>
      )}

      <div className="min-h-64 w-full">{children}</div>
    </section>
  )
}