from enum import Enum


class Gender(Enum):
    MASCULINE = "Masc"
    FEMININE = "Fem"
    NEUTER = "Neuter"
    UNKNOWN = "Unknown"

    @classmethod
    def values(cls) -> set[str]:
        return set(e.value for e in cls)

    @property
    def article(self) -> str:
        if self is self.MASCULINE:
            return "en"
        elif self is self.FEMININE:
            return "ei"
        elif self is self.NEUTER:
            return "et"
        else:
            return "et"