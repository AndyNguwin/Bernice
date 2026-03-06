from fastapi import APIRouter, Request
from server.security.discord_verify import verify_discord_signature
from server.handlers.drop import drop_handler
from server.handlers.inventory import inventory_handler

router = APIRouter()

@router.post("/interactions")
async def interactions(request: Request):
    print("Interactions reached")
    body = await request.body()

    verify_discord_signature(request, body)

    payload = await request.json()
    repository = request.app.state.repository

    interaction_type = payload["type"]
    if interaction_type == 1: # PING
        return {"type" : 1}
    elif interaction_type == 2: # Slash commands
        command = payload["data"]["name"]

        if command == "drop":
            return await drop_handler(payload, repository)
        elif command == "inventory":
            return await inventory_handler(payload, repository, 1, 4)

    elif interaction_type == 3: # Component clicks (like buttons)
        custom_id = payload["data"]["custom_id"]
        parts = custom_id.split(":")
        scope, user, action, current_page = parts

        if scope == "inventory":
            page = int(current_page)
            if action == "prev":
                return await inventory_handler(payload, repository, page=page - 1, response_type=7)
            else:
                return await inventory_handler(payload, repository, page=page + 1, response_type=7)

    elif interaction_type == 5: # modal/forms
        pass


    return {"type": 4, "data": {"content": "Unhandled."}}