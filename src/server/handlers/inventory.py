import math
from src.infra.db.postgres_repository import PostgresRepository
from src.app.models.inventoryCard import InventoryCard

async def inventory_handler(user_id: int, repository: PostgresRepository, owner_id=None, page=1, response_type=4):
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

    inventory_cards, inventory_count = await repository.get_user_inventory(user_id, page)

    inventory_text_list = []
    for card in inventory_cards:
        inventory_text_list.append(
            f"`{card.public_code:<6}` **{card.idol_name}** - {card.artist_name}  [{card.card_set}]  #{card.print_number}"
        )

    inventory_text_list.append(
        f"**Page {page} / {math.ceil(inventory_count / 10)}**"
    )
    
    inventory_text = "\n\n".join(inventory_text_list)

    return {
        "type": response_type,
        "data": {
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
    }
