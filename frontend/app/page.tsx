import { FeatureCard } from "@/components/feature-card";
import { PipelineStep } from "@/components/pipeline-step";
import { PrimaryButton } from "@/components/primary-button";
import { SecondaryButton } from "@/components/secondary-button";

const pipeline = [
  {
    title: "Capture",
    description: "Forward emails, receipts, and forms. Handled keeps everything in one queue."
  },
  {
    title: "Plan",
    description: "Agentic workflows draft steps, timelines, and dependencies before execution."
  },
  {
    title: "Execute",
    description: "Human-in-the-loop approvals and background jobs keep tasks moving."
  }
];

const features = [
  {
    title: "Magic-link onboarding",
    description: "Secure, passwordless access for clients and collaborators."
  },
  {
    title: "Workflow-ready backend",
    description: "Step-based execution with retries and human escalation built in."
  },
  {
    title: "AI co-pilot",
    description: "GPT-4o/5 models summarize, plan, and generate actionable briefs."
  }
];

export default function HomePage() {
  return (
    <main className="px-6 py-12 md:px-16 lg:px-24">
      <section className="max-w-4xl">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-handled-mint">
          Handled · Life Admin Execution
        </p>
        <h1 className="mt-4 text-4xl font-semibold md:text-6xl">
          Delegate the busywork. Keep the clarity.
        </h1>
        <p className="mt-6 text-lg text-slate-600">
          Handled combines AI planning with real execution workflows so you can offload
          appointments, follow-ups, travel logistics, and more.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <PrimaryButton label="Request early access" />
          <SecondaryButton label="View roadmap" />
        </div>
      </section>

      <section className="mt-16 grid gap-6 md:grid-cols-3">
        {pipeline.map((step) => (
          <PipelineStep key={step.title} {...step} />
        ))}
      </section>

      <section className="mt-16">
        <h2 className="text-2xl font-semibold">Why teams choose Handled</h2>
        <div className="mt-6 grid gap-6 md:grid-cols-3">
          {features.map((feature) => (
            <FeatureCard key={feature.title} {...feature} />
          ))}
        </div>
      </section>

      <section className="mt-16 rounded-3xl bg-white p-8 shadow-sm md:p-12">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Experience the guided task flow</h2>
            <p className="mt-2 text-sm text-slate-600">
              Each request moves through a single, focused flow from intake to completion.
            </p>
          </div>
          <PrimaryButton label="Start a task" />
        </div>
      </section>
    </main>
  );
}
