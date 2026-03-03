import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Butterfly Effect Simulator",
  description: "See how one small decision can change your entire life",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
