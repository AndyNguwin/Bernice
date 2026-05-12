from app.services.view import view_card
from infra.db.postgres_repository import PostgresRepository
from infra.discord.client import edit_deferred_message


async def view_handler(
    application_id: str,
    interaction_token: str,
    user_id: int,
    repository: PostgresRepository,
    public_code: str,
    interaction_id: str | None = None,
):
    card = await view_card(user_id, repository, public_code)
    if card is None:
        content = {
            "content": f"<@{user_id}>",
            "embeds": [
                {
                    "description": f"No card found for `{public_code}`.",
                }
            ],
        }
        await edit_deferred_message(
            application_id,
            interaction_token,
            content,
            interaction_id=interaction_id,
            interaction_name=f"view:{public_code}",
        )
        return

    description = f"""
        `Code:` {card.public_code}
        `Idol:` {card.idol_name}
        `Group/Solo:` {card.artist_name}
        `Set:` {card.card_set}
        `Rarity:` {card.rarity}
        `Your copies:` {card.quantity}
        `Total printed (global):` {card.total_print_count}
    """

    embed: dict = {"description": description}
    if card.image_url:
        embed["image"] = {"url": card.image_url}
    content = {"embeds": [embed]}

    await edit_deferred_message(
        application_id,
        interaction_token,
        content,
        interaction_id=interaction_id,
        interaction_name=f"view:{public_code}",
    )
