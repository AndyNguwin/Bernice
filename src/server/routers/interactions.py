import json
from fastapi import APIRouter, HTTPException, Request
from server.security.discord_verify import verify_discord_signature
from server.handlers.drop import drop_handler
from server.handlers.inventory import inventory_handler
from server.handlers.view import view_handler
from server.handlers.status import status_handler

router = APIRouter()

@router.post("/interactions")
async def interactions(request: Request):
    print("Interactions reached")
    body = await request.body()

    verify_discord_signature(request, body)

    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON")

    repository = request.app.state.repository

    try:
        interaction_type = payload["type"]
    except (KeyError, TypeError):
        raise HTTPException(400, "Missing field: type")
    

    if interaction_type == 1: # PING
        return {"type" : 1}
    
    try:
        user_id = int(payload["member"]["user"]["id"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(400, "Missing/invalid field: member.user.id")
        
    if interaction_type == 2: # Slash commands
        try:
            command = payload["data"]["name"]
        except (KeyError, TypeError):
            raise HTTPException(400, "Missing field: payload['data']['name']")

        if command == "drop":
            return await drop_handler(user_id, repository)
        elif command == "inventory":
            return await inventory_handler(user_id, repository, owner_id=None, page=1, response_type=4)
        elif command == "view":
            try:
                public_code = payload["data"]["options"][0]["value"]
                return await view_handler(user_id, repository, public_code)
            except (KeyError, TypeError, IndexError):
                raise HTTPException(400, "Missing field: options[0].value")
        elif command == "status":
            return await status_handler(user_id, response_type=4)
        
    elif interaction_type == 3: # Component clicks (like buttons)
        try:
            custom_id = payload["data"]["custom_id"]
        except (KeyError, TypeError):
            raise HTTPException(400, "Missing field: data.custom_id")

        parts = custom_id.split(":")
        scope = parts[0]

        if scope == "inventory":
            try:
                scope, owner_id, action, page = parts
                page = int(page)
            except (ValueError, TypeError):
                raise HTTPException(400, "Invalid inventory custom_id format")

            if action == "prev":
                return await inventory_handler(user_id, repository, owner_id=int(owner_id), page=page - 1, response_type=7)
            elif action == "next":
                return await inventory_handler(user_id, repository, owner_id=int(owner_id), page=page + 1, response_type=7)
            else:
                raise HTTPException(400, "Invalid inventory action")
        if scope == "status":
            return await status_handler(user_id, response_type=7)
            
    elif interaction_type == 5: # modal/forms
        pass


    return {"type": 4, "data": {"content": "Unhandled."}}