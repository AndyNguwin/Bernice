from src.infra.db.postgres_repository import PostgresRepository
from src.app.models.card import Card
from datetime import datetime

async def drop_handler(payload, repository: PostgresRepository):
    user_id = int(payload["member"]["user"]["id"])

    # Get random card logic
    # service layer

    # Placeholder
    # card_name = "NewJeans - Hanni (Common)"

    idol = await repository.get_random_idol()
    print_number = await repository.allocate_print(idol.idol_id)
    card_id = await repository.next_code()
    
    card = Card(
        card_id = card_id,
        idol_id = idol.idol_id,
        print_number = print_number,
        owner_id = user_id,
        acquired_date = datetime.now()
    )
    await repository.add_card_to_inventory(card)

    return {
        "type": 4,
        "data": {
            "content": f"<@{user_id}> pulled:\n **{idol.idol_name}**"
        }
    }