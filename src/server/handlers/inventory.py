from src.infra.db.postgres_repository import PostgresRepository
from src.app.models.inventoryCard import InventoryCard

async def inventory_handler(payload, repository):
    user_id = int(payload["member"]["user"]["id"])

    inventory_cards = await repository.get_user_inventory(user_id, 1)

    inventory_text_list = []
    for card in inventory_cards:
        inventory_text_list.append(
            f"`{card.public_code:<6}` **{card.idol_name}** - {card.artist_name}  [{card.card_set}]  #{card.print_number}"
        )
    
    inventory_text = "\n\n".join(inventory_text_list)

    return {
        "type": 4,
        "data": {
            "embeds": [
                {
                    "description" : inventory_text
                }
            ]
        }
    }
