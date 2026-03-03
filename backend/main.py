import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    GenerateRequest,
    GenerateResponse,
    GraphData,
    TimelineNode,
    NodePosition,
    NodeData,
    TimelineEdge,
    ImageRequest,
    ImageResponse,
)
from ai_service import generate_timeline
from graph_math import calculate_positions, generate_edges
from image_service import generate_image

app = FastAPI()

origins = ["http://localhost:3000", os.getenv("FRONTEND_URL", "")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "online", "engine": os.getenv("LLM_PROVIDER", "ollama")}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        raw_nodes = generate_timeline(request.user_decision)
        positioned = calculate_positions(raw_nodes)
        edges = generate_edges(positioned)

        nodes = [
            TimelineNode(
                id=n["id"],
                position=NodePosition(**n["position"]),
                data=NodeData(
                    year=n.get("year", ""),
                    event=n.get("event", ""),
                    impact=n.get("impact", "low"),
                ),
            )
            for n in positioned
        ]

        edge_models = [
            TimelineEdge(id=e["id"], source=e["source"], target=e["target"])
            for e in edges
        ]

        return GenerateResponse(
            status="success",
            data=GraphData(nodes=nodes, edges=edge_models),
        )

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-image", response_model=ImageResponse)
def generate_image_endpoint(request: ImageRequest):
    try:
        image_url = generate_image(request.final_event)
        return ImageResponse(status="success", image_url=image_url)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Local:  uvicorn main:app --host 127.0.0.1 --port 8000
# Render: uvicorn main:app --host 0.0.0.0 --port $PORT
