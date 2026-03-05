from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Card:
    card_id: int
    public_code: str
    idol_id: int
    print_number: int
    owner_id: int
    acquired_date: datetime