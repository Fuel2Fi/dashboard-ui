import * as React from "react"

export function Card({ className, ...props }) {
  return (
    <div
      className={`rounded-2xl border border-gray-200 bg-white p-4 shadow ${className}`}
      {...props}
    />
  )
}

export function CardContent({ className, ...props }) {
  return <div className={`mt-2 ${className}`} {...props} />
}
