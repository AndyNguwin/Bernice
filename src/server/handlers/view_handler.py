from app.services.view import view_card
from infra.db.postgres_repository import PostgresRepository
from infra.discord.client import edit_deferred_message
from datetime import datetime

async def view_handler(
    application_id: str,
    interaction_token: str,
    user_id:int ,
    repository: PostgresRepository,
    public_code:str,
    interaction_id: str | None = None,
):
    card = await view_card(user_id, repository, public_code)
    description = f"""
        `Code:` {card.public_code}
        `Idol:` {card.idol_name}
        `Group/Solo:` {card.artist_name}
        `Set Name:` {card.card_set}
        `Print #:` {card.print_number}
        `Owner:` <@{card.owner_id}>
        `Obtained:` {card.acquired_date.strftime("%b %d, %Y")}
    """

    content = {
        "embeds": [
            {
                "description": description,
                "image": {
                    "url": card.image_url
                }
            }
        ]
    }

    await edit_deferred_message(
        application_id,
        interaction_token,
        content,
        interaction_id=interaction_id,
        interaction_name=f"view:{public_code}",
    )
