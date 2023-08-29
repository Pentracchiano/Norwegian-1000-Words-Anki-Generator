from dataclasses import dataclass


class AttributedDataItem:
    def __init__(self, data: bytes, attribution: str):
        self.data = data
        self.attribution = attribution
        self.path = None

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.data)
        self.path = path
    
    def __repr__(self):
        return f"AttributedDataItem(data={'DATA' if self.data else 'None'}, attribution={self.attribution}, path={self.path})"


@dataclass
class NorwegianWord:
    norwegian: str
    pronunciation: AttributedDataItem
    article: str
    image: AttributedDataItem
    english: str
    frequency: int