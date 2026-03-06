from src.infra.db.postgres_repository import PostgresRepository
from src.app.models.inventoryCard import InventoryCard
from datetime import datetime

async def view_handler(user_id:int , repository: PostgresRepository, public_code:str):
    card: InventoryCard = await repository.get_card_by_public_code(public_code)
    description = f"""
        `Code:` {card.public_code}
        `Idol:` {card.idol_name}
        `Group/Solo:` {card.artist_name}
        `Set Name:` {card.card_set}
        `Print #:` {card.print_number}
        `Owner:` <@{card.owner_id}>
        `Obtained:` {card.acquired_date.strftime("%b %d, %Y")}
    """

    return {
        "type": 4,
        "data": {
            "embeds": [
                {
                    "description": description,
                    "image": {
                        "url": card.image_url
                    }
                }
            ]
        }
    }