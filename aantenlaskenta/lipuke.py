class Lipuke:
    ehdokkaat: list[int]
    jäljellä: float

    def __init__(self, ehdokkaat: list[int]):
        self.ehdokkaat = ehdokkaat
        self.jäljellä = 1.0
