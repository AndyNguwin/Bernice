from typing import Any, List, Dict, Tuple, Optional
import os
from dotenv import load_dotenv
import asyncpg
from app.models.idol import Idol
from app.models.card import Card
from app.models.user import User
from app.models.inventoryCard import InventoryCard

load_dotenv()
CONNECTION_STR = os.getenv("DATABASE_URL")
if not CONNECTION_STR:
    raise SystemExit("No DATABASE_URL in .env")

class PostgresRepository:
    def __init__(self):
        self.connection_str = CONNECTION_STR
        self._connection_pool = None

    async def _make_connection_pool(self) -> None:
        if self._connection_pool is None:
            self._connection_pool = await asyncpg.create_pool(
                self.connection_str,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
    
    def _check_pool_initialized(self) -> asyncpg.Pool:
        if not self._connection_pool:
            raise RuntimeError(
                "Connection pool not initialized yet."
            )
        return self._connection_pool
    
    def _encode_le_base36(self, n: int) -> str:
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

        if n == 0:
            return "0"
        out = []
        while n > 0:
            n, r = divmod(n, 36)
            out.append(ALPHABET[r])
        return "".join(out)  # little-endian: index0 cycles first

    async def next_public_code(self) -> str:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            code_count = await connection.fetchval("SELECT nextval('card_code_seq')")
        
        PRIME = 1000003
        ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
        # exclude the confusing characters and nums

        transformed = (code_count * PRIME) ^ (code_count >> 16)

        public_code = ""
        for i in range(6):
            char_index = transformed % len(ALPHABET)  # 55 instead of 32
            public_code = ALPHABET[char_index] + public_code
            transformed = transformed // len(ALPHABET)  # 55 instead of 32
        
        return public_code

    async def get_random_idol(self) -> Idol:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                idol = await connection.fetchrow(
                    "SELECT * FROM idol ORDER BY RANDOM() LIMIT 1"
                )
                # print(character)
                if not idol:
                    raise RuntimeError("Could not select an idol, check database")
                return Idol(
                    idol_id=idol["idol_id"],
                    idol_name=idol["idol_name"],
                    artist_id=idol["artist_id"],
                    card_set_id=idol["card_set_id"],
                    current_print=idol["current_print"],
                    image_url=idol["image_url"] 
                )
            except Exception as e:
                raise RuntimeError("Could not select an idol", e)
                
    async def allocate_print(self, idol_id: int) -> int:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                return await connection.fetchval(
                    """
                    UPDATE idol
                    SET current_print = current_print + 1
                    WHERE idol_id = $1
                    RETURNING current_print;
                    """,
                    idol_id
                )
        
            except Exception as e:
                raise RuntimeError("Error while allocating print", e)

    async def add_user(self, user_id: int) -> None:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                await connection.execute(
                    'INSERT INTO "user"(discord_id) VALUES($1)',
                    user_id
                )
            except Exception as e:
                raise RuntimeError(f"Error while inserting user {user_id}", e)

    async def get_user(self, user_id: int) -> Optional[User]:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                user = await connection.fetchrow(
                    'SELECT * FROM "user" WHERE discord_id = $1',
                    user_id
                )
                if not user:
                    return None
                
                return User(
                    user["discord_id"]
                    # user["discord_username"]
                )
            except Exception as e:
                raise RuntimeError("Error while finding user", e)

    async def get_user_inventory(self, user_id: int, page_num: int = 1) -> List[InventoryCard]:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                inventory_rows = await connection.fetch(
                    """
                    SELECT c.public_code, i.idol_name, a.artist_name, cs.card_set_name, c.print_number  
                    FROM card c
                    JOIN idol i ON c.idol_id = i.idol_id
                    JOIN artist a ON i.artist_id = a.artist_id
                    JOIN card_set cs ON i.card_set_id = cs.card_set_id
                    WHERE owner_id = $1
                    ORDER BY card_id ASC
                    LIMIT 10 OFFSET $2
                    """,
                    user_id,
                    (page_num - 1) * 10
                )

                inventory_cards = []
                for row in inventory_rows:
                    card = InventoryCard(
                        public_code = row["public_code"],
                        idol_name = row["idol_name"],
                        artist_name = row["artist_name"],
                        card_set = row["card_set_name"],
                        print_number = row["print_number"]
                    )
                    inventory_cards.append(card)
                
                return inventory_cards


            except Exception as e:
                raise RuntimeError("Error while checking inventory", e)
    
    async def get_card_by_public_code(self, public_code: str) -> Optional[InventoryCard]:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                row = await connection.fetchrow(
                    """
                    SELECT c.public_code, i.idol_name, a.artist_name, cs.card_set_name, c.print_number, c.owner_id, c.acquired_date, i.image_url
                    FROM card c
                    JOIN idol i ON c.idol_id = i.idol_id
                    JOIN artist a ON i.artist_id = a.artist_id
                    JOIN card_set cs ON i.card_set_id = cs.card_set_id
                    WHERE public_code = $1
                    """,
                    public_code,
                )

                if row:
                    return InventoryCard(
                        public_code = row["public_code"],
                        idol_name = row["idol_name"],
                        artist_name = row["artist_name"],
                        card_set = row["card_set_name"],
                        print_number = row["print_number"],
                        owner_id = row["owner_id"],
                        acquired_date = row["acquired_date"],
                        image_url = row["image_url"]
                    )
                else:
                    return None
            except Exception as e:
                raise RuntimeError("Error while viewing a card", e)

    
    async def get_artist_by_id(self, artist_id: int) -> str:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                artist_name = await connection.fetchval(
                    "SELECT artist_name FROM artist WHERE artist_id = $1",
                    artist_id
                )
                if not artist_name:
                    raise RuntimeError(f"Artist with id {artist_id} not found")
                return artist_name
            except Exception as e:
                raise RuntimeError(f"Error while fetching artist name for id {artist_id}", e)
    
    async def get_card_set_by_id(self, card_set_id: int) -> str:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                card_set = await connection.fetchval(
                    "SELECT card_set_name FROM card_set WHERE card_set_id = $1",
                    card_set_id
                )
                if not card_set:
                    raise RuntimeError(f"Card Set with id {card_set_id} not found")
                return card_set
            except Exception as e:
                raise RuntimeError(f"Error while fetching card set for id {card_set_id}", e)

    async def add_card_to_inventory(self, card: Card) -> int:
        pool = self._check_pool_initialized()
        
        async with pool.acquire() as connection:
            try:
                user = await self.get_user(card.owner_id)
                if not user:
                    await self.add_user(card.owner_id)

                card_id = await connection.fetchval(
                    """
                    INSERT INTO card(public_code, idol_id, print_number, owner_id)
                    VALUES ($1, $2, $3, $4)
                    RETURNING card_id
                    """,
                    card.public_code, card.idol_id, card.print_number, card.owner_id
                )

                return card_id
            except Exception as e:
                raise RuntimeError("Error while adding card to inventory", e)


    
