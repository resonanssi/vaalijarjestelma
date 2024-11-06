from enum import Enum


class Tila(Enum):
    Valittu = 1
    Toiveikas = 2
    Pudotettu = 3
    Jättäytynyt = 4


class Ehdokas:
    _id: int
    nimi: str
    painokerroin: float
    tila: Tila


    def __init__(self, nimi: str, _id: int):
        self.nimi = nimi
        self.tila = Tila.Toiveikas
        self.painokerroin = 1.0
        self._id = _id


    def __str__(self) -> str:
        return f"Ehdokas({self.nimi}, {self.tila}, {self.painokerroin}, {self._id})"
