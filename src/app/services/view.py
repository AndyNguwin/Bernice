from typing import Optional
from infra.db.postgres_repository import PostgresRepository
from app.models.inventoryCard import InventoryCard


async def view_card(
    user_id: int, repository: PostgresRepository, public_code: str
) -> Optional[InventoryCard]:
    return await repository.get_card(public_code, user_id)
