# 🚀 Local Discord Interactions Setup (FastAPI + ngrok)

## 1. Start the FastAPI server

From project root:

```bash
uvicorn src.server.main:app --reload --port 8000
```

Server runs at:

```
http://localhost:8000
```

---

## 2. Start ngrok tunnel

Authenticate once (after installing ngrok):

```bash
ngrok config add-authtoken YOUR_NGROK_TOKEN
```

Start tunnel:

```bash
ngrok http 8000
```

Copy the HTTPS URL shown, e.g.:

```
https://abc123.ngrok-free.app
```

---

## 3. Configure Discord Intera
