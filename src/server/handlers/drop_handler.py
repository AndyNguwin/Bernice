from app.services.drop import drop_card
from infra.db.postgres_repository import PostgresRepository
from infra.discord.client import edit_deferred_message

async def drop_handler(
    application_id: str,
    interaction_token: str,
    user_id: int,
    repository: PostgresRepository,
    interaction_id: str | None = None,
):
    drop_result = await drop_card(user_id, repository=repository)

    content = {
        "content": f"<@{user_id}>",
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

    await edit_deferred_message(
        application_id,
        interaction_token,
        content,
        interaction_id=interaction_id,
        interaction_name="drop",
    )
