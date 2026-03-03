"use client";

import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useEffect } from "react";
import NodeCard from "./NodeCard";
import type { TimelineNode, TimelineEdge } from "@/lib/types";

const nodeTypes = { custom: NodeCard };

interface TimelineGraphProps {
  nodes: TimelineNode[];
  edges: TimelineEdge[];
}

export default function TimelineGraph({ nodes: inputNodes, edges: inputEdges }: TimelineGraphProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  useEffect(() => {
    const flowNodes = inputNodes.map((n) => ({
      id: n.id,
      position: n.position,
      data: n.data as unknown as Record<string, unknown>,
      type: "custom" as const,
    }));

    const flowEdges: Edge[] = inputEdges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      animated: true,
      style: { stroke: "#a855f7", strokeWidth: 2 },
    }));

    setNodes(flowNodes);
    setEdges(flowEdges);
  }, [inputNodes, inputEdges, setNodes, setEdges]);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      nodeTypes={nodeTypes}
      fitView
      proOptions={{ hideAttribution: true }}
      className="bg-gray-950"
    />
  );
}
