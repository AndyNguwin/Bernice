import math
from typing import Tuple, List
from infra.db.postgres_repository import PostgresRepository
from app.models.inventoryCard import InventoryCard

async def view_inventory(user_id: int, repository: PostgresRepository, page=1) -> Tuple[List[InventoryCard], int]:
    return await repository.get_user_inventory(user_id, page)