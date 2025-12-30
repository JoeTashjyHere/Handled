import { PageShell } from "@/components/page-shell";
import { PrimaryButton } from "@/components/primary-button";

const checklist = [
  "Upload PDFs, images, or screenshots",
  "Add any key notes or constraints",
  "Confirm the request summary"
];

export default function UploadPage() {
  return (
    <PageShell
      eyebrow="Step 2"
      title="Upload your documents"
      description="Handled extracts details from your files and prepares the next steps."
    >
      <div className="grid gap-6 md:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-6 text-center shadow-sm">
          <p className="text-sm font-semibold">Drag & drop files here</p>
          <p className="mt-2 text-xs text-slate-500">PDF, JPG, PNG · up to 25MB</p>
          <PrimaryButton className="mt-4" label="Browse files" />
          <div className="mt-6 rounded-xl bg-slate-50 px-4 py-3 text-left text-xs text-slate-500">
            Recent uploads: Receipt_0424.pdf, Appointment.png
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-base font-semibold">Checklist</h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-600">
            {checklist.map((item) => (
              <li key={item} className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-handled-mint" />
                {item}
              </li>
            ))}
          </ul>
          <div className="mt-6 rounded-xl bg-handled-sand px-4 py-3 text-xs text-slate-600">
            Add a note: "This reimbursement is for June dentist visit."
          </div>
        </div>
      </div>
    </PageShell>
  );
}
