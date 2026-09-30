import type { TextareaHTMLAttributes } from 'react'

interface TextAreaProps
  extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helperText?: string
}

export default function TextArea({
  label,
  error,
  helperText,
  id,
  className = '',
  ...props
}: TextAreaProps) {
  const textareaId = id ?? props.name

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={textareaId}
          className="mb-1.5 block text-sm font-medium text-slate-700"
        >
          {label}
        </label>
      )}

      <textarea
        id={textareaId}
        className={`min-h-32 w-full resize-y rounded-lg border bg-white px-3 py-2.5 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:ring-2 ${
          error
            ? 'border-red-300 focus:border-red-400 focus:ring-red-100'
            : 'border-slate-300 focus:border-slate-400 focus:ring-slate-100'
        } ${className}`}
        aria-invalid={Boolean(error)}
        {...props}
      />

      {error ? (
        <p className="mt-1 text-xs text-red-600">{error}</p>
      ) : helperText ? (
        <p className="mt-1 text-xs text-slate-500">{helperText}</p>
      ) : null}
    </div>
  )
}