from typing import Dict, List, Tuple, Optional
import os
from dotenv import load_dotenv
import asyncpg
from app.models.idol_card_info import IdolCardInfo
from app.models.user import User
from app.models.inventoryCard import InventoryCard, InventoryListItem
import random

load_dotenv()
CONNECTION_STR = os.getenv("DATABASE_URL")
if not CONNECTION_STR:
    raise SystemExit("No DATABASE_URL in .env")

GUILD = os.getenv("GUILD")
if not GUILD:
    GUILD = None

class PostgresRepository:
    def __init__(self):
        self.connection_str = CONNECTION_STR
        self._connection_pool = None
        self.rarity_rates: Dict[int, float] = {}

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

    async def load_rarity_rates(self) -> None:
        pool = self._check_pool_initialized()
        async with pool.acquire() as connection:
            try:
                rows = await connection.fetch(
                    """
                    SELECT rarity, rate
                    FROM rarity_rates
                    ORDER BY rarity
                    """
                )

                self.rarity_rates = {
                    row["rarity"]: float(row["rate"])
                    for row in rows
                }
            except Exception as e:
                raise RuntimeError("Could not load rarity rates", e)

    async def get_random_idol_card(self, guild_id: str = None) -> IdolCardInfo:
        pool = self._check_pool_initialized()
        if not self.rarity_rates:
            await self.load_rarity_rates()

        rarity = random.choices(
            population=list(self.rarity_rates.keys()),
            weights=list(self.rarity_rates.values()),
            k=1
        )[0]

        if rarity == 5:
            if GUILD and guild_id and guild_id == GUILD and random.random() < 0.20:
                rarity = 6
            else:
                rarity = random.choice([1, 2, 3])
        elif rarity == 4:
            # No 4-star cards in the current catalog, route those drops into the existing 1-3 pool
            rarity = random.choice([1, 2, 3])

        # Plan to make 4 stars before 5 stars, temporary solution where I can delete the 4 star branch later on

        async with pool.acquire() as connection:
            try:
                row = await connection.fetchrow(
                    """
                    SELECT ic.idol_card_id, ic.public_code, ic.image_url,
                           i.idol_name, a.artist_name, cs.card_set_name, ic.rarity
                    FROM idol_card ic
                    JOIN idol i ON ic.idol_id = i.idol_id
                    JOIN artist a ON i.artist_id = a.artist_id
                    JOIN card_set cs ON ic.card_set_id = cs.card_set_id
                    WHERE ic.rarity = $1
                    ORDER BY RANDOM() LIMIT 1
                    """,
                    rarity,
                )
                if not row:
                    raise RuntimeError("Could not select a card, check idol_card catalog")
                return IdolCardInfo(
                    idol_card_id=row["idol_card_id"],
                    public_code=row["public_code"],
                    idol_name=row["idol_name"],
                    artist_name=row["artist_name"],
                    card_set=row["card_set_name"],
                    rarity=row["rarity"],
                    image_url=row["image_url"] or "",
                )
            except Exception as e:
                raise RuntimeError("Could not select an idol_card", e)

    async def grant_drop(self, user_id: int, idol_card_id: int) -> Tuple[int, int]:
        """Increment print count and user inventory. Returns total_print_count and user's card quantity."""
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                async with connection.transaction():
                    user = await connection.fetchrow(
                        'SELECT discord_id FROM "user" WHERE discord_id = $1',
                        user_id,
                    )
                    if not user:
                        await connection.execute(
                            'INSERT INTO "user"(discord_id) VALUES($1)',
                            user_id,
                        )

                    total = await connection.fetchval(
                        """
                        UPDATE idol_card
                        SET total_print_count = total_print_count + 1
                        WHERE idol_card_id = $1
                        RETURNING total_print_count
                        """,
                        idol_card_id,
                    )
                    if total is None:
                        raise RuntimeError(f"idol_card_id {idol_card_id} not found")

                    quantity = await connection.fetchval(
                        """
                        INSERT INTO user_inventory (user_id, idol_card_id, quantity)
                        VALUES ($1, $2, 1)
                        ON CONFLICT (user_id, idol_card_id)
                        DO UPDATE SET quantity = user_inventory.quantity + 1
                        RETURNING quantity
                        """,
                        user_id,
                        idol_card_id,
                    )
                return int(total), int(quantity)
            except Exception as e:
                raise RuntimeError("Error while granting drop", e)

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
                )
            except Exception as e:
                raise RuntimeError("Error while finding user", e)

    async def get_user_inventory(
        self, user_id: int, page_num: int = 1
    ) -> Tuple[List[InventoryListItem], int, int, int]:
        """
        Paginated inventory for Discord.

        Returns:
            - Rows for this page: public_code, idol (member), artist (group), quantity each.
            - total_copies: SUM(quantity) — total cards the user holds.
            - line_count: number of distinct catalog lines (pagination count, page size 10).
            - effective_page: clamped page in [1, total_pages] so OFFSET is never past the end.
        """
        pool = self._check_pool_initialized()
        page_size = 10

        async with pool.acquire() as connection:
            try:
                total_copies = await connection.fetchval(
                    """
                    SELECT COALESCE(SUM(quantity), 0)::bigint
                    FROM user_inventory
                    WHERE user_id = $1
                    """,
                    user_id,
                )
                line_count = await connection.fetchval(
                    """
                    SELECT COUNT(*)::bigint
                    FROM user_inventory
                    WHERE user_id = $1
                    """,
                    user_id,
                )

                line_count = int(line_count or 0)
                total_copies = int(total_copies or 0)
                total_pages = max(1, (line_count + page_size - 1) // page_size) if line_count else 1
                page_num = page_num if page_num >= 1 else 1
                if page_num > total_pages:
                    page_num = total_pages

                inventory_rows = await connection.fetch(
                    """
                    SELECT ic.public_code, i.idol_name, a.artist_name, ui.quantity
                    FROM user_inventory ui
                    JOIN idol_card ic ON ui.idol_card_id = ic.idol_card_id
                    JOIN idol i ON ic.idol_id = i.idol_id
                    JOIN artist a ON i.artist_id = a.artist_id
                    WHERE ui.user_id = $1
                    ORDER BY ic.public_code
                    LIMIT $2 OFFSET $3
                    """,
                    user_id,
                    page_size,
                    (page_num - 1) * page_size,
                )

                inventory_cards: List[InventoryListItem] = []
                for row in inventory_rows:
                    inventory_cards.append(
                        InventoryListItem(
                            public_code=row["public_code"],
                            idol_name=row["idol_name"],
                            artist_name=row["artist_name"],
                            quantity=row["quantity"],
                        )
                    )

                return (inventory_cards, total_copies, line_count, page_num)

            except Exception as e:
                raise RuntimeError("Error while checking inventory", e)
    
    async def get_card(self, public_code: str, user_id: int) -> Optional[InventoryCard]:
        pool = self._check_pool_initialized()

        async with pool.acquire() as connection:
            try:
                row = await connection.fetchrow(
                    """
                    SELECT ic.public_code, i.idol_name, a.artist_name, cs.card_set_name,
                           ic.rarity, ic.total_print_count,
                           COALESCE(ui.quantity, 0) AS quantity,
                           ic.image_url
                    FROM idol_card ic
                    JOIN idol i ON ic.idol_id = i.idol_id
                    JOIN artist a ON i.artist_id = a.artist_id
                    JOIN card_set cs ON ic.card_set_id = cs.card_set_id
                    LEFT JOIN user_inventory ui
                        ON ui.idol_card_id = ic.idol_card_id AND ui.user_id = $2
                    WHERE ic.public_code = $1
                    """,
                    public_code,
                    user_id,
                )

                if not row:
                    return None
                return InventoryCard(
                    public_code=row["public_code"],
                    idol_name=row["idol_name"],
                    artist_name=row["artist_name"],
                    card_set=row["card_set_name"],
                    rarity=row["rarity"],
                    quantity=row["quantity"],
                    total_print_count=row["total_print_count"],
                    image_url=row["image_url"],
                )
            except Exception as e:
                raise RuntimeError("Error while viewing a card", e)
