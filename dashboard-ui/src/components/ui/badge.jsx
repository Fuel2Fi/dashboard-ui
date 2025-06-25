import * as React from "react"

export function Badge({ className = "", children, ...props }) {
  return (
    <span
      className={`inline-flex items-center rounded-md bg-zinc-100 px-2 py-1 text-sm font-medium text-zinc-800 ring-1 ring-inset ring-zinc-200 ${className}`}
      {...props}
    >
      {children}
    </span>
  )
}
