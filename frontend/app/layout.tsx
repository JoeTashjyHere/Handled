import "./globals.css";

export const metadata = {
  title: "Handled · AI Life Admin",
  description: "AI-powered life admin execution app for delegating, tracking, and completing tasks."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        {children}
      </body>
    </html>
  );
}
