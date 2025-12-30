import { PageShell } from "@/components/page-shell";
import { PrimaryButton } from "@/components/primary-button";

export default function LoginPage() {
  return (
    <PageShell
      eyebrow="Magic link"
      title="Sign in to Handled"
      description="We'll send a secure link to your email so you can resume your active task."
    >
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <label className="text-sm font-medium text-slate-700" htmlFor="email">
          Email address
        </label>
        <input
          id="email"
          type="email"
          placeholder="you@company.com"
          className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm"
        />
        <div className="mt-4 flex flex-wrap gap-3">
          <PrimaryButton label="Send magic link" />
          <button className="text-sm font-semibold text-slate-500">Use a different account</button>
        </div>
      </div>
      <p className="mt-4 text-xs text-slate-500">
        By continuing, you agree to receive emails for task updates and approvals.
      </p>
    </PageShell>
  );
}
