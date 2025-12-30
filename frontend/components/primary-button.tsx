import type { ButtonHTMLAttributes } from "react";

interface PrimaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
}

export function PrimaryButton({ label, className = "", ...props }: PrimaryButtonProps) {
  return (
    <button
      className={`rounded-full bg-handled-ink px-6 py-3 text-sm font-semibold text-white ${className}`}
      {...props}
    >
      {label}
    </button>
  );
}
