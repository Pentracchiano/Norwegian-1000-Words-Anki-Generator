from dataclasses import dataclass


@dataclass
class NorwegianWord:
    norwegian: str
    pronunciation: str
    article: str
    image: str
    english: str
    frequency: int
