"use client";

import { useEffect, useState } from "react";
import { api, apiUpload } from "@/lib/api";
import { useParams, useRouter } from "next/navigation";

export default function TaskPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const taskId = params.id;

  const [task, setTask] = useState<any>(null);
  const [err, setErr] = useState("");
  const [uploading, setUploading] = useState(false);

  async function load() {
    setErr("");
    try {
      const t = await api(`/tasks/${taskId}`);
      setTask(t);
    } catch {
      router.replace("/");
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [taskId]);

  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files?.[0]) return;
    setUploading(true);
    setErr("");
    try {
      await apiUpload(`/tasks/${taskId}/upload`, e.target.files[0]);
      await load();
    } catch (e: any) {
      setErr(e.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function tick() {
    await api(`/tasks/${taskId}/tick`, { method: "POST", body: "{}" });
    await load();
  }

  if (!task) return <div className="text-slate-600">Loading…</div>;

  const timeline: string[] = task.steps?.timeline || [];
  const files: any[] = task.steps?.files || [];

  return (
    <div className="space-y-6">
      <div className="space-y-2 rounded-2xl border p-4">
        <div className="text-lg font-semibold">{task.title}</div>
        <div className="text-sm text-slate-600">{task.description}</div>
        <div className="text-sm">
          <span className="text-slate-500">Type:</span> {task.task_type}
        </div>
        <div className="text-sm">
          <span className="text-slate-500">Status:</span> {task.status}
        </div>
      </div>

      <div className="space-y-3 rounded-2xl border p-4">
        <div className="font-medium">Upload documents</div>
        <input type="file" onChange={onFile} disabled={uploading} />
        {files.length > 0 && (
          <div className="text-sm text-slate-600">
            Uploaded: {files.map((f) => f.filename).join(", ")}
          </div>
        )}
        <button className="rounded-xl border px-3 py-2" onClick={tick}>
          Run next step
        </button>
        <div className="text-xs text-slate-500">
          MVP note: “Run next step” simulates agent workflow ticks. Replace with background jobs
          later.
        </div>
        {err && <div className="text-sm text-red-600">{err}</div>}
      </div>

      <div className="space-y-2 rounded-2xl border p-4">
        <div className="font-medium">Status timeline</div>
        <div className="space-y-2">
          {timeline.length === 0 && <div className="text-sm text-slate-600">No updates yet.</div>}
          {timeline.map((t, i) => (
            <div key={i} className="text-sm text-slate-700">
              • {t}
            </div>
          ))}
        </div>
      </div>

      <div className="space-y-2 rounded-2xl border p-4">
        <div className="font-medium">Artifacts (debug)</div>
        <pre className="overflow-auto rounded-xl bg-slate-50 p-3 text-xs">
{JSON.stringify(task.steps?.artifacts || {}, null, 2)}
        </pre>
      </div>
    </div>
  );
}
