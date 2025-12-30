import { PageShell } from "@/components/page-shell";
import { PrimaryButton } from "@/components/primary-button";
import { StepCard } from "@/components/step-card";

const taskOptions = [
  {
    title: "HSA/FSA reimbursement",
    description: "Upload receipts and we prepare the claim packet.",
    meta: "Reimbursement"
  },
  {
    title: "Scheduling assistance",
    description: "Coordinate meetings with your availability and preferences.",
    meta: "Scheduling"
  },
  {
    title: "Government form help",
    description: "We gather the details and prep your submission checklist.",
    meta: "Forms"
  },
  {
    title: "Simple tax filing",
    description: "Collect documents and prep a straightforward filing flow.",
    meta: "Taxes"
  }
];

export default function TaskSelectionPage() {
  return (
    <PageShell
      eyebrow="Step 1"
      title="Choose your task"
      description="Handled guides one task at a time. Pick the request you want to start."
    >
      <div className="grid gap-4 md:grid-cols-2">
        {taskOptions.map((task) => (
          <StepCard key={task.title} {...task} />
        ))}
      </div>
      <div className="mt-8 flex flex-wrap gap-4">
        <PrimaryButton label="Continue to upload" />
        <button className="text-sm font-semibold text-slate-500">Save for later</button>
      </div>
    </PageShell>
  );
}
