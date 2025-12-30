interface StepCardProps {
  title: string;
  description: string;
  meta?: string;
}

export function StepCard({ title, description, meta }: StepCardProps) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      {meta ? <p className="text-xs font-semibold uppercase text-slate-400">{meta}</p> : null}
      <h3 className="mt-2 text-lg font-semibold">{title}</h3>
      <p className="mt-3 text-sm text-slate-600">{description}</p>
    </article>
  );
}
