from app.services.drop import drop_card
from infra.db.postgres_repository import PostgresRepository

async def drop_handler(user_id: int, repository: PostgresRepository):
    drop_result = await drop_card(user_id, repository=repository)

    return {
        "type": 4,
        "data": {
            # "content": f"<@{user_id}> pulled:\n **{idol.idol_name}**",
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
    }