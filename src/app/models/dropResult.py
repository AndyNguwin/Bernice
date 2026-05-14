from dataclasses import dataclass


@dataclass(frozen=True)
class DropResult:
    public_code: str
    idol_name: str
    artist_name: str
    card_set: str
    rarity: int
    image_url: str
    total_print_count: int
    quantity: int
