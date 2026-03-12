## Bernice (Discord Interactions + FastAPI)

Bernice is a Discord gacha-style card collection bot implemented using **Discord Interactions (webhooks)** backed by a **FastAPI** server and **PostgreSQL**.

### Project structure

- **`src/server/`**: HTTP boundary (FastAPI app + routers + request verification + Discord response formatting)
- **`src/infra/`**: infrastructure adapters (DB access, external services)
- **`src/app/`**: application/domain layer (models today; use-cases can live here as the project grows)
- **`init/`**: SQL init scripts used by Postgres container
- **`tests/`**: tests (WIP)
- **`register_commands.py`**: registers slash commands with Discord (guild-scoped in dev)

### Prerequisites

- **Python** 3.10+ (3.12 is fine)
- **PostgreSQL** (local) OR Docker + Docker Compose (recommended for local dev DB)
- **ngrok** (or any HTTPS tunnel) for local Discord webhook testing

### Environment variables

Create a `.env` at repo root (used by the FastAPI server and `register_commands.py`).

- **Discord**
  - `DISCORD_APPLICATION_ID`
  - `DISCORD_TOKEN` (bot token; used by `register_commands.py`)
  - `DISCORD_PUBLIC_KEY` (for signature verification)
- **Database** (used by `src/infra/db/postgres_repository.py`)
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`
  - `POSTGRES_DB`
  - (and whatever host/port variable your repository expects; see `src/infra/db/postgres_repository.py`)

### Local setup (recommended)

From the repo root (PowerShell):

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

**Why `pip install -e .`?** It makes `server`, `app`, and `infra` importable without needing `src.` prefixes or setting `PYTHONPATH`.

### Run local dev

#### 1) Start Postgres (Docker)

```bash
docker-compose up -d db
```

#### 2) Start the FastAPI server

```bash
python -m uvicorn server.main:app --reload --port 8000
```
or
```bash
uvicorn server.main:app --reload --port 8000
```

Open `http://localhost:8000/docs` to confirm it booted.

#### 3) Expose localhost to Discord (ngrok)
Typically have to use a git bash terminal
```bash
ngrok http 8000
```

Copy the **HTTPS** forwarding URL and paste it into:
**Discord Developer Portal → Application → Interactions Endpoint URL**

#### 4) Register slash commands

```bash
python register_commands.py
```

### Available commands (slash)

- **`/drop`**: roll a random idol card
- **`/inventory`**: view your inventory (paginated)
- **`/view code:<public_code>`**: view a specific card by code
- **`/status`**: creator-only (toggles status response)

### Deploy (Render)

**Start command:**

```bash
uvicorn server.main:app --host 0.0.0.0 --port $PORT
```

**Test locally (prod-like bind):**

```bash
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### Troubleshooting

#### `ModuleNotFoundError: No module named 'server'`

Make sure you ran:

```bash
pip install -e .
```

and start the app like:

```bash
python -m uvicorn server.main:app --reload --port 8000
```

#### Imports are inconsistent (`src.` vs no `src.`)

Pick one style and apply it everywhere. This repo is set up for **no `src.`** imports when installed into a venv with `pip install -e .`.
