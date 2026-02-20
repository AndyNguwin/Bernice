from fastapi import APIRouter, Request
from ..security.discord_verify import verify_discord_signature

router = APIRouter()

@router.post("/interactions")
async def interactions(request: Request):
    body = await request.body()

    verify_discord_signature(request, body)

    payload = await request.json()

    if payload["type"] == 1:
        return {"type" : 1}

    return {"type": 4, "data": {"content": "Unhandled."}}