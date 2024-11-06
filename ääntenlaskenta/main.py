from enum import Enum

class Tila(Enum):
    Valittu = 1
    Toiveikas = 2
    Pudotettu = 3

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

class Lipuke:
    ehdokkaat: list[int]
    jäljellä: float

    def __init__(self, ehdokkaat: list[int]):
        self.ehdokkaat = ehdokkaat
        self.jäljellä = 1.0

def lue_lipukkeet(syöte: list[str]) -> tuple[str, int, list[Ehdokas], list[Lipuke]]:
    iteraattori = iter(map(str.strip, syöte))

    ehdokasmäärä, paikkamäärä = [int(x) for x in next(iteraattori).split()]

    lipukkeet = []
    while (rivi := next(iteraattori)) != "0":
        osat = rivi.split()[1:-1]
        ids = [int(x) for x in osat]
        lipukkeet.append(Lipuke(ids))

    ehdokkaat = []
    i = 1
    while i <= ehdokasmäärä:
        nimi = next(iteraattori)[1:-1]
        ehdokkaat.append(Ehdokas(nimi, i))
        i += 1

    vaalin_nimi = next(iteraattori)[1:-1]
    
    return (vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet)

if __name__ == "__main__":

    with open("testivaali.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_lipukkeet(f.readlines())

    print(vaalin_nimi)

    print()
    print("Ehdokkaat:")

    for ehdokas in ehdokkaat:
        print(ehdokas)

