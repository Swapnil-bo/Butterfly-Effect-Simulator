export type ImpactLevel = 'low' | 'medium' | 'high' | 'life-changing';

export interface TimelineNodeData {
  year: string;
  event: string;
  impact: ImpactLevel;
  imageUrl?: string;
  isFinalNode?: boolean;
}

export interface TimelineNode {
  id: string;
  position: { x: number; y: number };
  data: TimelineNodeData;
}

export interface TimelineEdge {
  id: string;
  source: string;
  target: string;
}

export interface GenerateResponse {
  status: string;
  data: {
    nodes: TimelineNode[];
    edges: TimelineEdge[];
  };
}
