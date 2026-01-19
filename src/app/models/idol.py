from dataclasses import dataclass

@dataclass(frozen=True)
class Idol:
    idol_id: int
    idol_name: str
    artist_id: int
    card_set_id: int
    current_print: int
    image_url: str