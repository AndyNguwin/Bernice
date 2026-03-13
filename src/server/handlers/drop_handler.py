from app.services.drop import drop_card
from infra.db.postgres_repository import PostgresRepository
import httpx

async def drop_handler(application_id: str, interaction_token: str, user_id: int, repository: PostgresRepository):
    drop_result = await drop_card(user_id, repository=repository)

    content = {
        "embeds": [
            {
                "title": f"{drop_result.idol_name} — {drop_result.artist_name} [{drop_result.card_set}]",
                "description": f"Rolled by <@{user_id}>",
                "image": {
                    "url": drop_result.image_url
                },
                "footer": {
                    "text": f"Code {drop_result.public_code} • Print {drop_result.print_number}"
                }
            }
        ]
    }

    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}/messages/@original"
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=content)
        response.raise_for_status()