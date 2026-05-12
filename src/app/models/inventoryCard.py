from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InventoryListItem:
    """One row in the paginated inventory list (code, member, group, copy count)."""

    public_code: str
    idol_name: str
    artist_name: str
    quantity: int


@dataclass(frozen=True)
class InventoryCard:
    public_code: str
    idol_name: str
    artist_name: str
    card_set: str
    rarity: int
    quantity: int
    total_print_count: Optional[int] = None
    image_url: Optional[str] = None
