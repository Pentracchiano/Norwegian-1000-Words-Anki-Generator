from enum import Enum


class Gender(Enum):
    MASCULINE = "Masc"
    FEMININE = "Fem"
    NEUTER = "Neuter"
    UNKNOWN = "Unknown"

    @classmethod
    def values(cls) -> set[str]:
        return set(e.value for e in cls)

