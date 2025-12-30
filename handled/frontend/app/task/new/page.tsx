"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

type TaskType = "reimbursement" | "scheduling" | "government_form" | "tax_filing";

export default function NewTaskPage() {
  const router = useRouter();
  const [email, setEmail] = useState<string>("");
  const [taskType, setTaskType] = useState<TaskType>("reimbursement");
  const [title, setTitle] = useState("Get reimbursed (HSA/FSA)");
  const [description, setDescription] = useState("");
  const [err, setErr] = useState("");

  useEffect(() => {
    api("/me")
      .then((u) => setEmail(u.email))
      .catch(() => router.replace("/"));
  }, [router]);

  async function createTask() {
    setErr("");
    try {
      const t = await api("/tasks", {
        method: "POST",
        body: JSON.stringify({ task_type: taskType, title, description }),
      });
      router.push(`/task/${t.id}`);
    } catch (e: any) {
      setErr(e.message || "Failed to create task");
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-sm text-slate-500">Signed in as {email}</div>

      <div className="space-y-3 rounded-2xl border p-4">
        <div className="font-medium">What do you want handled?</div>

        <select
          className="w-full rounded-xl border px-3 py-2"
          value={taskType}
          onChange={(e) => {
            const v = e.target.value as TaskType;
            setTaskType(v);
            if (v === "reimbursement") setTitle("Get reimbursed (HSA/FSA)");
            if (v === "scheduling") setTitle("Book an appointment");
            if (v === "government_form") setTitle("Submit a government form");
            if (v === "tax_filing") setTitle("File my taxes (simple)");
          }}
        >
          <option value="reimbursement">Reimbursement (HSA/FSA)</option>
          <option value="scheduling">Scheduling</option>
          <option value="government_form">Government forms</option>
          <option value="tax_filing">Tax filing</option>
        </select>

        <input
          className="w-full rounded-xl border px-3 py-2"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
        />

        <textarea
          className="min-h-[100px] w-full rounded-xl border px-3 py-2"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Anything we should know? (optional)"
        />

        <button className="w-full rounded-xl bg-slate-900 py-2 text-white" onClick={createTask}>
          Create task
        </button>

        {err && <div className="text-sm text-red-600">{err}</div>}
      </div>
    </div>
  );
}
