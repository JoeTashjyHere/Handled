"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter, useSearchParams } from "next/navigation";

export default function LoginPage() {
  const sp = useSearchParams();
  const router = useRouter();
  const token = sp.get("token");

  const [msg, setMsg] = useState("Signing you in…");

  useEffect(() => {
    async function run() {
      if (!token) {
        setMsg("Missing token.");
        return;
      }
      try {
        await api("/auth/verify-magic-link", {
          method: "POST",
          body: JSON.stringify({ token }),
        });
        router.replace("/task/new");
      } catch (e: any) {
        setMsg(e.message || "Login failed.");
      }
    }
    run();
  }, [token, router]);

  return <div className="text-slate-700">{msg}</div>;
}
