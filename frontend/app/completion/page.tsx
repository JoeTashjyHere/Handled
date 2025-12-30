import { PageShell } from "@/components/page-shell";
import { PrimaryButton } from "@/components/primary-button";

export default function CompletionPage() {
  return (
    <PageShell
      eyebrow="Complete"
      title="All set"
      description="Your request has been executed and a confirmation email is on the way."
    >
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-handled-mint/10 text-2xl">
          ✓
        </div>
        <h2 className="mt-4 text-xl font-semibold">Reimbursement submitted</h2>
        <p className="mt-2 text-sm text-slate-600">
          We'll notify you when the claim is approved and funds are on the way.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <PrimaryButton label="Start another task" />
          <button className="text-sm font-semibold text-slate-500">View status</button>
        </div>
      </div>
    </PageShell>
  );
}
