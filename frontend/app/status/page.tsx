import { PageShell } from "@/components/page-shell";

const timeline = [
  {
    title: "Intake received",
    description: "Documents and notes have been captured.",
    status: "Complete"
  },
  {
    title: "Eligibility review",
    description: "Verifying reimbursement policy and documentation.",
    status: "In progress"
  },
  {
    title: "Submission prep",
    description: "Preparing claim packet and confirmation email.",
    status: "Queued"
  }
];

export default function StatusPage() {
  return (
    <PageShell
      eyebrow="Tracking"
      title="Your task is in motion"
      description="Handled updates you after every step so you know what's happening."
    >
      <div className="space-y-4">
        {timeline.map((item) => (
          <div key={item.title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-semibold">{item.title}</h3>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                {item.status}
              </span>
            </div>
            <p className="mt-2 text-sm text-slate-600">{item.description}</p>
          </div>
        ))}
      </div>
    </PageShell>
  );
}
