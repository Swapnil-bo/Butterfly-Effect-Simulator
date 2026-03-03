"use client";

import { useState } from "react";
import TimelineGraph from "@/components/TimelineGraph";
import LoadingState from "@/components/LoadingState";
import type { TimelineNode, TimelineEdge } from "@/lib/types";

export default function Home() {
  const [decision, setDecision] = useState("");
  const [nodes, setNodes] = useState<TimelineNode[]>([]);
  const [edges, setEdges] = useState<TimelineEdge[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasGenerated, setHasGenerated] = useState(false);

  const handleGenerate = async () => {
    if (!decision.trim()) return;
    setLoading(true);
    setError("");

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const res = await fetch(`${apiUrl}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_decision: decision }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const json = await res.json();
      setNodes(json.data.nodes);
      setEdges(json.data.edges);
      setHasGenerated(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center px-4 py-12">
      <h1 className="text-4xl font-bold mb-2 text-center">
        Butterfly Effect Simulator
      </h1>
      <p className="text-gray-400 mb-8 text-center max-w-md">
        Enter a small life decision and watch it spiral into something
        extraordinary over 10 years.
      </p>

      <div className="flex gap-3 w-full max-w-xl mb-8">
        <input
          type="text"
          value={decision}
          onChange={(e) => setDecision(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
          placeholder="e.g. I bought a cheap guitar at a thrift store"
          className="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700
                     text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
          disabled={loading}
        />
        <button
          onClick={handleGenerate}
          disabled={loading || !decision.trim()}
          className="px-6 py-3 rounded-lg bg-purple-600 hover:bg-purple-700
                     font-semibold disabled:opacity-50 disabled:cursor-not-allowed
                     transition-colors"
        >
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg px-5 py-4 mb-6 max-w-xl w-full">
          <p className="text-red-400 font-medium mb-1">Generation failed</p>
          <p className="text-red-300 text-sm">{error}</p>
          <button
            onClick={handleGenerate}
            className="mt-3 text-sm text-red-400 hover:text-red-300 underline"
          >
            Try again
          </button>
        </div>
      )}

      {loading && <LoadingState />}

      {hasGenerated && !loading && !error && nodes.length < 2 && (
        <div className="text-gray-500 text-center py-12">
          <p className="text-lg mb-1">Not enough data to build a timeline.</p>
          <p className="text-sm">Try a different decision and generate again.</p>
        </div>
      )}

      {hasGenerated && !loading && !error && nodes.length >= 2 && (
        <div className="w-full" style={{ height: "70vh" }}>
          <TimelineGraph nodes={nodes} edges={edges} />
        </div>
      )}
    </main>
  );
}
