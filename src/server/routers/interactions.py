from fastapi import APIRouter, Request
from server.security.discord_verify import verify_discord_signature
from server.handlers.drop import drop_handler
from server.handlers.inventory import inventory_handler
from src.server.handlers.view import view_handler
from src.server.routers.status import status_handler

router = APIRouter()

@router.post("/interactions")
async def interactions(request: Request):
    print("Interactions reached")
    body = await request.body()

    verify_discord_signature(request, body)

    payload = await request.json()
    repository = request.app.state.repository

    user_id = int(payload["member"]["user"]["id"])
    interaction_type = payload["type"]
    
    if interaction_type == 1: # PING
        return {"type" : 1}
    elif interaction_type == 2: # Slash commands
        command = payload["data"]["name"]

        if command == "drop":
            return await drop_handler(user_id, repository)
        elif command == "inventory":
            return await inventory_handler(user_id, repository, owner_id=None, page=1, response_type=4)
        elif command == "view":
            public_code = payload["data"]["options"][0]["value"]
            return await view_handler(user_id, repository, public_code)
        elif command == "status":
            return await status_handler(user_id, response_type=4)
        
    elif interaction_type == 3: # Component clicks (like buttons)
        custom_id = payload["data"]["custom_id"]
        parts = custom_id.split(":")
        scope = parts[0]

        if scope == "inventory":
            scope, owner_id, action, page = parts
            page = int(page)
            if action == "prev":
                return await inventory_handler(user_id, repository, owner_id=int(owner_id), page=page - 1, response_type=7)
            else:
                return await inventory_handler(user_id, repository, owner_id=int(owner_id), page=page + 1, response_type=7)

        if scope == "status":
            return await status_handler(user_id, response_type=7)
            
    elif interaction_type == 5: # modal/forms
        pass


    return {"type": 4, "data": {"content": "Unhandled."}}