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
        "content": f"<@{user_id}'s drop result!>",
        "embeds": [
            {
                "title": f"{drop_result.artist_name} {drop_result.idol_name}",
                "description": (
                    f"✦ ```{drop_result.public_code}```\n"
                    f"✦ Type: {drop_result.card_set}\n"
                    f"✦ Rarity: {drop_result.rarity}\n"
                    f"✦ In Inventory: {drop_result.quantity}\n"
                    f"✦ Total printed: {drop_result.total_print_count}"
                ),
                "image": {
                    "url": drop_result.image_url
                },
                # "footer": {
                #     "text": f"Code {drop_result.public_code} - Total printed {drop_result.total_print_count}"
                # }
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
