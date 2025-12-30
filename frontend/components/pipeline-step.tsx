interface PipelineStepProps {
  title: string;
  description: string;
}

export function PipelineStep({ title, description }: PipelineStepProps) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <p className="text-sm font-semibold text-handled-mint">{title}</p>
      <p className="mt-3 text-base text-slate-600">{description}</p>
    </div>
  );
}
