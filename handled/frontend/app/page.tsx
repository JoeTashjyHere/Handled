"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function Home() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [err, setErr] = useState("");

  async function requestLink() {
    setErr("");
    await api("/auth/request-magic-link", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
    setSent(true);
  }

  return (
    <div className="space-y-6">
      <div className="text-xl font-medium">We handle your paperwork.</div>
      <div className="text-slate-600">
        Upload receipts, book appointments, submit government forms, file simple taxes — with
        approval-first execution.
      </div>

      <div className="space-y-3 rounded-2xl border p-4">
        <div className="text-sm font-medium">Get started</div>
        <input
          className="w-full rounded-xl border px-3 py-2"
          placeholder="you@work.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button
          className="w-full rounded-xl bg-slate-900 py-2 text-white"
          onClick={requestLink}
          disabled={!email}
        >
          Send magic link
        </button>
        {sent && (
          <div className="text-sm text-slate-600">
            Link sent. In dev, check your backend console for the URL.
          </div>
        )}
        {err && <div className="text-sm text-red-600">{err}</div>}
      </div>

      <div className="text-sm text-slate-500">
        Already have a link? Open it and you’ll be signed in.
      </div>
    </div>
  );
}
