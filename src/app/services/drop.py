from app.models.dropResult import DropResult
from infra.db.postgres_repository import PostgresRepository


async def drop_card(user_id: int, repository: PostgresRepository, guild_id: str = None) -> DropResult:
    card = await repository.get_random_idol_card(guild_id)
    total_print_count, quantity = await repository.grant_drop(user_id, card.idol_card_id)

    return DropResult(
        public_code=card.public_code,
        idol_name=card.idol_name,
        artist_name=card.artist_name,
        card_set=card.card_set,
        rarity=card.rarity,
        image_url=card.image_url,
        total_print_count=total_print_count,
        quantity=quantity,
    )
