import type { ReactNode } from "react";

interface PageShellProps {
  eyebrow?: string;
  title: string;
  description?: string;
  children: ReactNode;
}

export function PageShell({ eyebrow, title, description, children }: PageShellProps) {
  return (
    <main className="min-h-screen px-6 py-12 md:px-16 lg:px-24">
      <section className="max-w-4xl">
        {eyebrow ? (
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-handled-mint">
            {eyebrow}
          </p>
        ) : null}
        <h1 className="mt-4 text-3xl font-semibold md:text-5xl">{title}</h1>
        {description ? (
          <p className="mt-4 text-base text-slate-600 md:text-lg">{description}</p>
        ) : null}
      </section>
      <section className="mt-10 max-w-4xl">{children}</section>
    </main>
  );
}
