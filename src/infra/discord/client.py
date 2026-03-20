import httpx

async def edit_deferred_message(application_id: str, interaction_token: str, content) -> None:
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}/messages/@original"
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=content)
        response.raise_for_status()