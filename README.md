# Butterfly Effect Simulator

**What if one small decision changed your entire life?**

Type a mundane life decision. Watch AI generate a logical but wild chain of 5-7 escalating life events over 10 years, rendered as an interactive visual timeline.

**[Live Demo](https://butterfly-effect-simulator.vercel.app)**

---

## How It Works

1. You enter a small decision: *"I bought a cheap guitar at a thrift store"*
2. An LLM generates a believable butterfly effect chain of escalating consequences
3. Each event is classified by impact level: `low` → `medium` → `high` → `life-changing`
4. The chain is rendered as an interactive graph with color-coded nodes and animated edges

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│                   (Vercel / Next.js)                     │
│                                                         │
│  ┌──────────┐   ┌────────────────┐   ┌──────────────┐  │
│  │ page.tsx  │──▶│ TimelineGraph  │──▶│   NodeCard    │  │
│  │ (input)   │   │ (React Flow)   │   │ (styled node) │  │
│  └────┬─────┘   └────────────────┘   └──────────────┘  │
│       │                                                  │
└───────┼──────────────────────────────────────────────────┘
        │  POST /generate
        │  { "user_decision": "..." }
        ▼
┌─────────────────────────────────────────────────────────┐
│                      BACKEND                            │
│                  (Render / FastAPI)                      │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │ prompt_builder│──▶│  ai_service   │──▶│ graph_math │  │
│  │ (system prompt│   │ (LLM client + │   │ (positions │  │
│  │  + few-shot)  │   │  retry logic) │   │  + edges)  │  │
│  └──────────────┘   └──────┬───────┘   └────────────┘  │
│                             │                            │
└─────────────────────────────┼────────────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │      LLM PROVIDER     │
                  │                       │
                  │  Local: Ollama        │
                  │         Qwen 2.5 3B   │
                  │                       │
                  │  Prod:  Groq API      │
                  │         Llama 3.1 8B  │
                  └───────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | Next.js 14 + TypeScript + Tailwind CSS | App Router for modern React patterns, Tailwind for rapid UI, TypeScript for type safety across the API contract |
| **Graph** | React Flow (@xyflow/react) | Purpose-built for node-edge graphs with built-in pan/zoom, `useNodesState`/`useEdgesState` hooks eliminate external state management |
| **Backend** | Python + FastAPI | Async-ready, auto-generates OpenAPI docs, Pydantic models enforce the API contract at both serialization and validation |
| **Local AI** | Ollama + Qwen 2.5 3B | Runs on 3GB VRAM, fast enough for dev iteration, returns structured JSON reliably with proper prompting |
| **Production AI** | Groq API + Llama 3.1 8B | Free tier, sub-second inference, identical OpenAI SDK interface — zero code changes to switch from local |
| **Deploy** | Vercel (frontend) + Render (backend) | Free tier on both, Vercel auto-detects Next.js, Render runs Python with a simple start command |

### Key Design Decisions

**Dual LLM strategy** — Local Ollama for development (no API costs, works offline), Groq for production (fast, free tier). Both use the OpenAI Python SDK. Switching is a single environment variable (`LLM_PROVIDER=ollama` vs `groq`).

**Structured AI output** — The LLM prompt uses a system message with schema definition, impact level constraints, and a complete few-shot example (both input and output). This achieves 10/10 reliability for valid JSON responses from a 3B parameter model.

**Retry with validation** — `ai_service.py` retries up to 3 times if the LLM returns invalid JSON or the wrong number of nodes (must be 5-7). This makes the pipeline robust without needing a larger model.

**No Zustand** — React Flow's built-in `useNodesState` and `useEdgesState` hooks handle all graph state. Adding a state management library for a single-page app would be over-engineering.

---

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.ai) with Qwen 2.5 3B pulled: `ollama pull qwen2.5:3b`

### Backend

```bash
cd backend
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env: set LLM_PROVIDER=ollama (default for local dev)

# Start the server
uvicorn main:app --host 127.0.0.1 --port 8000
```

Verify: `curl http://127.0.0.1:8000/health` should return `{"status": "online", "engine": "ollama"}`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and enter a decision.

---

## Deployment

### Backend (Render)

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repo
3. Configure:
   - **Root directory:** `backend`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables:
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_key_from_console.groq.com
   FRONTEND_URL=https://your-app.vercel.app
   ```

### Frontend (Vercel)

1. Import the repo on [Vercel](https://vercel.com)
2. Set **Root directory** to `frontend`
3. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```

---

## API Endpoints

### `GET /health`
```json
{ "status": "online", "engine": "groq" }
```

### `POST /generate`
```json
// Request
{ "user_decision": "I bought a cheap acoustic guitar at a thrift store." }

// Response
{
  "status": "success",
  "data": {
    "nodes": [
      {
        "id": "node-1",
        "position": { "x": 250, "y": 0 },
        "data": { "year": "Year 1", "event": "You learn three chords...", "impact": "low" }
      }
    ],
    "edges": [
      { "id": "e1-2", "source": "node-1", "target": "node-2" }
    ]
  }
}
```

### `POST /generate-image`
```json
// Request
{ "final_event": "You headline a sold-out world tour." }

// Response
{ "status": "success", "image_url": "data:image/png;base64,..." }
```

---

## Project Structure

```
butterfly-effect-simulator/
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router (page, layout, styles)
│   │   ├── components/       # TimelineGraph, NodeCard, LoadingState
│   │   └── lib/              # TypeScript types, API helpers
│   ├── package.json
│   └── vercel.json
├── backend/
│   ├── main.py               # FastAPI app with CORS + endpoints
│   ├── models.py             # Pydantic request/response models
│   ├── ai_service.py         # LLM client (Ollama/Groq) + retry logic
│   ├── prompt_builder.py     # System prompt + few-shot example
│   ├── graph_math.py         # Node positioning + edge generation
│   ├── image_service.py      # Together.ai image generation
│   └── requirements.txt
└── README.md
```

---

## Built By

**Swapnil** — targeting AI/ML Product Management internships. This project demonstrates structured AI data generation, interactive graph visualization, and full-stack deployment with a dual-LLM architecture.
