from pydantic import BaseModel


class GenerateRequest(BaseModel):
    user_decision: str


class NodePosition(BaseModel):
    x: float
    y: float


class NodeData(BaseModel):
    year: str
    event: str
    impact: str  # "low" | "medium" | "high" | "life-changing"


class TimelineNode(BaseModel):
    id: str
    position: NodePosition
    data: NodeData


class TimelineEdge(BaseModel):
    id: str
    source: str
    target: str


class GraphData(BaseModel):
    nodes: list[TimelineNode]
    edges: list[TimelineEdge]


class GenerateResponse(BaseModel):
    status: str
    data: GraphData
