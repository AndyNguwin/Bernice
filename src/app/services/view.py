from infra.db.postgres_repository import PostgresRepository
from app.models.inventoryCard import InventoryCard

async def view_card(user_id:int , repository: PostgresRepository, public_code:str) -> InventoryCard:
    card = await repository.get_card_by_public_code(public_code)

    return card