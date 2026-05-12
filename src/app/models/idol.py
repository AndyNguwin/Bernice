from dataclasses import dataclass


@dataclass(frozen=True)
class Idol:
    idol_id: int
    idol_name: str
    artist_id: int
