import { PageShell } from "@/components/page-shell";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";

const extractedFields = [
  { label: "Provider", value: "Brightline Dental" },
  { label: "Date of service", value: "06/14/2024" },
  { label: "Amount", value: "$245.00" },
  { label: "Category", value: "Dental" }
];

export default function ApprovalPage() {
  return (
    <PageShell
      eyebrow="Step 3"
      title="Approve extracted details"
      description="Review the data Handled pulled from your documents before we proceed."
    >
      <div className="grid gap-6 md:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-base font-semibold">Extracted fields</h3>
          <dl className="mt-4 space-y-3 text-sm">
            {extractedFields.map((field) => (
              <div key={field.label} className="flex items-center justify-between">
                <dt className="text-slate-500">{field.label}</dt>
                <dd className="font-medium text-slate-900">{field.value}</dd>
              </div>
            ))}
          </dl>
          <div className="mt-6 rounded-xl bg-slate-50 px-4 py-3 text-xs text-slate-600">
            AI reasoning: Matches a dental reimbursement receipt with a clear provider and amount.
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-base font-semibold">Next actions</h3>
          <p className="mt-2 text-sm text-slate-600">
            Approving will send this data into the reimbursement workflow.
          </p>
          <div className="mt-6 flex flex-col gap-3">
            <PrimaryButton label="Approve & continue" />
            <SecondaryButton label="Edit details" />
            <button className="text-sm font-semibold text-rose-500">Reject request</button>
          </div>
        </div>
      </div>
    </PageShell>
  );
}
