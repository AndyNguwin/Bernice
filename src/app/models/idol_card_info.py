from dataclasses import dataclass


@dataclass(frozen=True)
class IdolCardInfo:
    idol_card_id: int
    public_code: str
    idol_name: str
    artist_name: str
    card_set: str
    rarity: int
    image_url: str
