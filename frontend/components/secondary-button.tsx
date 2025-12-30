import type { ButtonHTMLAttributes } from "react";

interface SecondaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
}

export function SecondaryButton({ label, className = "", ...props }: SecondaryButtonProps) {
  return (
    <button
      className={`rounded-full border border-handled-ink px-6 py-3 text-sm font-semibold ${className}`}
      {...props}
    >
      {label}
    </button>
  );
}
