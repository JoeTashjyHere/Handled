const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function api(path: string, opts: RequestInit = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...opts,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(opts.headers || {}),
    },
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || `Request failed: ${res.status}`);
  }
  return res.json();
}

export async function apiUpload(path: string, file: File) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    body: form,
    credentials: "include",
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || `Upload failed: ${res.status}`);
  }
  return res.json();
}
