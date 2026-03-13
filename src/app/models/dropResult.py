from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DropResult:
    public_code: str
    print_number: int
    idol_name: str
    artist_name: str
    card_set: str
    image_url: str