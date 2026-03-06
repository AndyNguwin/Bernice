from src.infra.db.postgres_repository import PostgresRepository
from src.app.models.inventoryCard import InventoryCard

async def view_handler(user_id:int , public_code:str, repository: PostgresRepository):
    card: InventoryCard = await repository.get_card_by_public_code(public_code)

    return {
        "type": 4,
        "data": {
            "embeds": [
                {
                    "title": f"{card.idol_name} — {card.artist_name} [{card.card_set}]",
                    "description": f"Rolled by <@{card.owner_id}>",
                    "image": {
                        "url": card.image_url
                    },
                    "footer": {
                        "text": f"Code {public_code} • Print {card.print_number}"
                    }
                }
            ]
        }
    }