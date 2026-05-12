from app.services.inventory import view_inventory
from infra.db.postgres_repository import PostgresRepository
from infra.discord.client import edit_deferred_message


async def inventory_handler(
    application_id: str,
    interaction_token: str,
    user_id: int,
    repository: PostgresRepository,
    owner_id=None,
    page=1,
    response_type=4,
    interaction_id: str | None = None,
):
    # Response 4: new message
    # Response 7: edit message
    if response_type == 7 and owner_id != user_id:
        return {
            "type": 4,
            "data": {
                "flags": 64, # only the wrong user who clicks sees it (ephemeral)
                "content": "This inventory belongs to someone else."
            }
        }

    target_id = owner_id if owner_id is not None else user_id
    inventory_cards, total_copies, line_count, effective_page = await view_inventory(
        target_id, repository, page=page
    )

    page_size = 10
    total_pages = max(1, (line_count + page_size - 1) // page_size) if line_count else 1

    if not inventory_cards and line_count == 0:
        inventory_text = "*No cards yet.*"
    else:
        lines = []
        for card in inventory_cards:
            lines.append(
                f"`{card.public_code}` · **{card.idol_name}** · {card.artist_name} · **×{card.quantity}**"
            )
        lines.append(f"— Page **{effective_page}** / **{total_pages}** —")
        inventory_text = "\n".join(lines)

    content = {
        "content": f"<@{target_id}>'s Inventory",
        "embeds": [
            {
                "title": f"Total cards: {total_copies}",
                "description": inventory_text
            }
        ],
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 2,
                        "label": "Previous",
                        "custom_id": f"inventory:{target_id}:prev:{effective_page}",
                        "disabled": effective_page <= 1
                    },
                    {
                        "type": 2,
                        "style": 2,
                        "label": "Next",
                        "custom_id": f"inventory:{target_id}:next:{effective_page}",
                        "disabled": effective_page >= total_pages
                    }
                ]
            }
        ]
    }

    interaction_name = "inventory_page"
    if response_type == 4:
        interaction_name = "inventory"

    await edit_deferred_message(
        application_id,
        interaction_token,
        content,
        interaction_id=interaction_id,
        interaction_name=interaction_name,
    )
