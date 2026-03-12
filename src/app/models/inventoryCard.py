from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass(frozen=True)
class InventoryCard:
    public_code: str
    idol_name: str
    artist_name: str
    card_set: str 
    print_number: int
    owner_id: Optional[int] = None
    acquired_date: Optional[datetime] = None
    image_url: Optional[str] = None