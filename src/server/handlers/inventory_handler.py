import math
from app.services.inventory import view_inventory
from infra.db.postgres_repository import PostgresRepository
from app.models.inventoryCard import InventoryCard
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

    inventory_cards, inventory_count = await view_inventory(user_id, repository, page=page)

    inventory_text_list = []
    for card in inventory_cards:
        inventory_text_list.append(
            f"`{card.public_code:<6}` **{card.idol_name}** - {card.artist_name}  [{card.card_set}]  #{card.print_number}"
        )

    inventory_text_list.append(
        f"**Page {page} / {math.ceil(inventory_count / 10)}**"
    )
    
    inventory_text = "\n\n".join(inventory_text_list)

    content = {
        "content": f"<@{user_id}>'s Inventory",
        "embeds": [
            {
                "title" : f"Inventory: {inventory_count} total cards",
                "description" : inventory_text
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
                        "custom_id": f"inventory:{user_id}:prev:{page}",
                        "disabled": page <= 1
                    },
                    {
                        "type": 2,
                        "style": 2,
                        "label": "Next",
                        "custom_id": f"inventory:{user_id}:next:{page}",
                        "disabled": len(inventory_text_list) < 10
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
