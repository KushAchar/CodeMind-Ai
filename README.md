# CodeMind-Ai

An AI-powered developer assistant that understands software repositories and
helps developers explore, analyze, debug, and understand unfamiliar codebases
using Retrieval-Augmented Generation (RAG).

## Project structure

```text
codemind-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── chat.py
│   │   │       ├── health.py
│   │   │       ├── ingestion.py
│   │   │       └── repositories.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── qdrant.py
│   │   │   └── session.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai/
│   │   │   └── rag/
│   │   └── main.py
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── .env.example
│   ├── requirements-dev.txt
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Backend responsibilities

- `app/main.py`: creates the FastAPI application and registers middleware and
  route modules.
- `app/api/`: HTTP-only concerns. `dependencies.py` contains reusable
  dependency injection providers; `routes/` groups endpoints by feature.
- `app/core/`: cross-cutting concerns such as typed environment settings,
  structured logging, and security utilities.
- `app/db/`: infrastructure adapters for PostgreSQL sessions and Qdrant.
  `base.py` is the SQLAlchemy model registry.
- `app/models/`: database persistence models only. They describe stored data
  and relationships, not API payloads.
- `app/schemas/`: Pydantic request and response contracts. Keeping these
  separate from ORM models prevents persistence details leaking into the API.
- `app/services/`: use-case orchestration independent of HTTP. Top-level
  services coordinate application workflows.
- `app/services/ai/`: Groq, LangChain, prompts, and LangGraph workflows.
  These adapters can evolve without changing route handlers.
- `app/services/rag/`: repository loading, parsing, chunking, embeddings,
  Qdrant retrieval, reranking, and context selection.
- `tests/unit/`: isolated tests for services and adapters.
- `tests/integration/`: tests that exercise PostgreSQL, Qdrant, or API
  boundaries.
- `requirements.txt`: runtime Python dependencies.
- `requirements-dev.txt`: test, lint, and development dependencies.
- `.env.example`: safe configuration template; real `.env` files stay local.

## PostgreSQL and Qdrant integration

The backend uses SQLAlchemy's reusable `engine` and `SessionLocal` factory in
`backend/app/db/session.py`. FastAPI handlers can request a session with
`Depends(get_db)` from `backend/app/api/dependencies.py`; no repository or
user tables are created by this integration.

Qdrant is provided by the cached client in `backend/app/db/qdrant.py`.
Configure both services with `DATABASE_URL` and `QDRANT_URL` in the backend
environment. The `/api/health` endpoint is a liveness check, while
`/api/health/ready` verifies PostgreSQL with `SELECT 1` and Qdrant by listing
collections. Readiness returns HTTP 200 when both are reachable and HTTP 503
with per-service statuses otherwise.

The LLM integration is provider-independent through the `LLMService` protocol
in `backend/app/services/ai/llm.py`. The current `GroqLLMService` uses
`GROQ_API_KEY` and `GROQ_MODEL` and is exposed through `POST /api/llm/test`.
Keys are only passed to the SDK and are never included in API responses or
logs. Missing configuration and provider failures return a safe `503` error.

Test with Postman:

1. Copy `backend/.env.example` to `backend/.env`, set `GROQ_API_KEY`, and
   choose a valid `GROQ_MODEL`.
2. Start the API from `backend` with `uvicorn app.main:app --reload`.
3. Create a `POST` request to `http://localhost:8000/api/llm/test`.
4. Set `Content-Type: application/json`.
5. Send the raw JSON body:

   ```json
   {
     "message": "Explain what REST API is"
   }
   ```

On success, the response has the form
`{"success": true, "response": "Generated LLM response"}`. Do not put the API
key in the request body or commit the local `.env` file.

## Public GitHub repository integration

`POST /api/repositories/connect` accepts a public GitHub repository URL and
returns metadata from the GitHub REST API. It currently does not download
repository files, create database records, or run RAG/embedding workflows.

The implementation is split into:

- `backend/app/api/routes/repositories.py`: validates the HTTP request and maps
  service errors to `422`, `404`, and `503` responses.
- `backend/app/schemas/github.py`: defines the typed request and metadata
  response contracts used by FastAPI and OpenAPI.
- `backend/app/services/github.py`: validates `github.com/{owner}/{repo}`
  URLs, calls `/repos/{owner}/{repo}`, and maps GitHub fields to the API model.
- `backend/app/core/config.py`: configures the GitHub API URL, timeout, and
  optional token. A token is never returned in API responses.

Postman test:

1. Start the API from `backend` with `uvicorn app.main:app --reload`.
2. Create a `POST` request to
   `http://localhost:8000/api/repositories/connect`.
3. Set `Content-Type` to `application/json`.
4. Send:

   ```json
   {
     "repository_url": "https://github.com/KushAchar/CodeMind-Ai"
   }
   ```

5. A successful response contains `name`, `description`,
   `primary_language`, `default_branch`, `stars`, `forks`, and
   `repository_url`. Invalid GitHub URLs return `422`, missing or private
   repositories return `404`, and GitHub/network failures return `503`.

## Frontend responsibilities

- `src/components/`: reusable presentational React components.
- `src/pages/`: route-level screens.
- `src/services/`: API clients and backend communication.
- `src/hooks/`: reusable React state and data-fetching hooks.
- `src/types/`: shared TypeScript contracts.
- `src/lib/`: small framework-agnostic utilities.
- `public/`: static assets served unchanged by Vite.
- `package.json`: frontend scripts and dependencies.
- `vite.config.js`: Vite build and development-server configuration.

## Root infrastructure

- `docker-compose.yml`: local PostgreSQL and Qdrant infrastructure with
  persistent named volumes.
- `.gitignore`: excludes secrets, generated files, caches, and dependencies.

The empty implementation modules intentionally contain only package markers or
short module descriptions. Feature code should be added behind the boundaries
described above rather than placing database, AI, and HTTP logic in one file.

## Initial FastAPI API

Run the backend from the `backend` directory:

```powershell
uvicorn app.main --reload
```

The initial endpoints are:

- `GET /`: returns the application welcome message and version.
- `GET /api/health`: returns the service health status and version.
- `POST /api/repositories/connect`: returns metadata for a public GitHub
  repository.

`app/main.py` creates the FastAPI application, loads settings, configures
logging, enables CORS for local React development servers, registers routers,
and converts validation and unexpected failures into JSON responses.
`app/api/router.py` composes versioned API routers, while each feature route
module owns its endpoint definitions. `app/schemas/common.py` defines typed
Pydantic response models so the OpenAPI contract and runtime responses stay
consistent.

## Local infrastructure

The root `docker-compose.yml` runs PostgreSQL and Qdrant with named volumes.
Create a local environment file first:

```powershell
Copy-Item .env.example .env
# Edit .env and replace POSTGRES_PASSWORD with a strong local password.
```

Start the services in the background:

```powershell
docker compose up -d
```

Check container status and health:

```powershell
docker compose ps
docker compose logs --follow postgres qdrant
```

Stop the containers while preserving data:

```powershell
docker compose stop
```

Stop and remove the containers and network while preserving named volumes:

```powershell
docker compose down
```

Remove the containers and permanently delete local database/vector data:

```powershell
docker compose down -v
```

PostgreSQL is available on port `5432`; Qdrant exposes HTTP on `6333` and
gRPC on `6334`. The Compose file requires `POSTGRES_PASSWORD`, while the
remaining values have safe local-development defaults and can be overridden
through `.env`.

Run the backend tests from `backend`:

```powershell
pytest
```

For a live connectivity check, start the Compose services, copy
`backend/.env.example` to `backend/.env`, set the PostgreSQL password in the
URL, and request:

```powershell
Invoke-RestMethod http://localhost:8000/api/health/ready
```
