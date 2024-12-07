from enum import Enum


class Tila(Enum):
    Valittu = 1
    Toiveikas = 2
    Pudotettu = 3
    Jättäytynyt = 4

    def __str__(self):
        return self.name


class Ehdokas:
    _id: int
    nimi: str
    painokerroin: float
    tila: Tila
    summa: float
    pudotusvertailu_summa: float

    def __init__(self, nimi: str, _id: int):
        self.nimi = nimi
        self.tila = Tila.Toiveikas
        self.painokerroin = 1.0
        self._id = _id
        self.summa = 0.0
        self.pudotusvertailu_summa = 0.0

    def __str__(self) -> str:
        return f"[{self._id}]: {self.nimi}"

    def __repr__(self) -> str:
        return f"Ehdokas({self._id}, {self.nimi}, {self.tila.name}, summa={self.summa})"

    def valitse(self):
        self.tila = Tila.Valittu

    def pudota(self):
        self.tila = Tila.Pudotettu

    def alusta_painokerroin(self):
        match self.tila:
            case Tila.Pudotettu:
                self.painokerroin = 0.0
            case Tila.Toiveikas:
                self.painokerroin = 1.0
            case _:
                pass
