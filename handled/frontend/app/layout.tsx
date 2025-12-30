import "./globals.css";
import React from "react";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-slate-900">
        <div className="mx-auto max-w-xl p-6">
          <div className="mb-8">
            <div className="text-2xl font-semibold">Handled</div>
            <div className="text-sm text-slate-500">Life admin, executed.</div>
          </div>
          {children}
        </div>
      </body>
    </html>
  );
}
