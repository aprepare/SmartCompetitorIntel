# SmartCompetitorIntel

SmartCompetitorIntel is a FastAPI-based RAG service for competitor intelligence. It turns product, marketing, and social-media notes into a searchable knowledge base, then answers analysis questions with retrieved sources and streaming LLM responses.

The current version focuses on Chinese competitor-research workflows and ships with mock data so contributors can run the full pipeline locally before connecting real crawlers.

## Why This Project Exists

Competitor analysis is often scattered across spreadsheets, screenshots, social posts, and ad-hoc notes. This project provides a small, inspectable open-source foundation for:

- importing competitor notes into a vector knowledge base;
- retrieving relevant evidence for a question;
- generating answers that are grounded in retrieved data;
- returning source snippets so analysts can verify the answer;
- extending the system with real crawlers, scheduled reports, and dashboard UI.

## Features

- RAG question answering with ChromaDB vector search.
- Streaming and non-streaming chat responses.
- Chinese embedding model support through `BAAI/bge-small-zh-v1.5`.
- FastAPI endpoints with OpenAPI documentation.
- Mock competitor data for local development.
- Modular app layout for crawlers, document processing, retrieval, and LLM services.

## Tech Stack

| Area | Technology |
| --- | --- |
| API server | FastAPI, Uvicorn |
| LLM client | OpenAI Python SDK with an OpenAI-compatible base URL |
| Vector store | ChromaDB |
| Embeddings | Sentence Transformers, bge-small-zh |
| Text processing | LangChain text splitters |
| Config | Pydantic Settings |

## Repository Layout

```text
SmartCompetitorIntel/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── rag/
│   ├── services/
│   └── crawler/
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` and set your API key.

The project currently uses DeepSeek defaults because it exposes an OpenAI-compatible API. You can point the same client at another OpenAI-compatible endpoint by changing `DEEPSEEK_BASE_URL` and `DEEPSEEK_MODEL`.

### 4. Start the API server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open the API docs at:

```text
http://localhost:8000/docs
```

### 5. Load mock data and ask a question

```bash
curl -X POST http://localhost:8000/api/v1/crawl
```

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "哪个赛道互动量最高？", "stream": false}'
```

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/chat` | RAG chat with optional SSE streaming |
| `POST` | `/api/v1/crawl` | Import mock competitor data |
| `GET` | `/api/v1/knowledge/stats` | Show vector-store status |
| `POST` | `/api/v1/knowledge/clear` | Clear the knowledge base |

## Current Status

This repository is an early-stage open-source project. The core backend pipeline is in place:

- mock data ingestion;
- document chunking;
- vector storage and retrieval;
- grounded LLM response generation;
- FastAPI service endpoints.

The next milestone is to replace mock inputs with real, permission-aware data connectors and add a small UI for analysts.

## Roadmap

- Add connector interfaces for user-provided competitor data exports.
- Add scheduled daily and weekly intelligence reports.
- Add Redis-backed conversation memory.
- Add Docker and docker-compose deployment.
- Add tests for retrieval, prompt grounding, and API behavior.
- Add a lightweight dashboard for uploading notes and reviewing sources.

## Good First Issues

- Add unit tests for `DocumentProcessor`.
- Add a `/api/v1/knowledge/search` endpoint for debugging retrieval results.
- Add Docker support.
- Improve `.env.example` with provider-specific examples.
- Add sample request/response fixtures for the API docs.

## How Codex Can Help Maintain This Project

This project is a good fit for AI-assisted open-source maintenance because it has clear, testable development tasks:

- writing tests around RAG retrieval and API behavior;
- reviewing prompt changes for hallucination risk;
- refactoring provider configuration while keeping backward compatibility;
- adding documentation examples and troubleshooting notes;
- implementing small roadmap items without blocking maintainers.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).
