from app.models.dropResult import DropResult
from infra.db.postgres_repository import PostgresRepository
from app.models.card import Card
from datetime import datetime

async def drop_card(user_id: int, repository: PostgresRepository):
    idol = await repository.get_random_idol()
    print_number = await repository.allocate_print(idol.idol_id)
    public_code = await repository.next_public_code()
    artist = await repository.get_artist_by_id(idol.artist_id)
    card_set = await repository.get_card_set_by_id(idol.card_set_id)
    
    card = Card(
        card_id = 0,
        public_code = public_code,
        idol_id = idol.idol_id,
        print_number = print_number,
        owner_id = user_id,
        acquired_date = datetime.now()
    )
    card_id = await repository.add_card_to_inventory(card)

    return DropResult(
        public_code=public_code,
        print_number=print_number,
        idol_name=idol.idol_name,
        artist_name=artist,
        card_set=card_set,
        image_url=idol.image_url
    )