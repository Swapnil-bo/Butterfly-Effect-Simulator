"use client";

import { Handle, Position, type NodeProps } from "@xyflow/react";
import type { TimelineNodeData } from "@/lib/types";

const impactColors: Record<string, string> = {
  low: "border-green-500",
  medium: "border-yellow-500",
  high: "border-orange-500",
  "life-changing": "border-purple-500",
};

const impactBadgeColors: Record<string, string> = {
  low: "bg-green-500/20 text-green-400",
  medium: "bg-yellow-500/20 text-yellow-400",
  high: "bg-orange-500/20 text-orange-400",
  "life-changing": "bg-purple-500/20 text-purple-400",
};

export default function NodeCard({ data }: NodeProps) {
  const { year, event, impact, imageUrl, isFinalNode } =
    data as unknown as TimelineNodeData;
  const borderColor = impactColors[impact] || "border-gray-600";
  const badgeColor = impactBadgeColors[impact] || "bg-gray-500/20 text-gray-400";

  return (
    <div
      className={`bg-gray-900 border-2 ${borderColor} rounded-xl px-5 py-4
                  max-w-xs shadow-lg`}
    >
      <Handle type="target" position={Position.Top} className="opacity-0" />

      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-bold text-gray-300">{year}</span>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${badgeColor}`}>
          {impact}
        </span>
      </div>

      <p className="text-sm text-gray-100 leading-relaxed">{event}</p>

      {isFinalNode && !imageUrl && (
        <div className="mt-3 w-full h-40 bg-gradient-to-br from-purple-900/40 to-indigo-900/40
                        border border-purple-500/20 rounded-lg flex flex-col items-center justify-center gap-2">
          <span className="text-3xl">🎨</span>
          <p className="text-purple-300 text-xs font-medium">AI Image Coming Soon</p>
        </div>
      )}

      {isFinalNode && imageUrl && (
        <img
          src={imageUrl}
          alt={event}
          className="mt-3 w-full rounded-lg"
        />
      )}

      <Handle type="source" position={Position.Bottom} className="opacity-0" />
    </div>
  );
}
