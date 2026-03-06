from dataclasses import dataclass

@dataclass(frozen=True)
class InventoryCard:
    public_code: str
    idol_name: str
    artist_name: str
    card_set: str 
    print_number: int