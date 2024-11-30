from dataclasses import dataclass
from ehdokas import Ehdokas


class VaaliLogger:
    tapahtumat: list[str]

    def __init__(self):
        self.tapahtumat = []

    def lisää(self, tapahtuma: str):
        self.tapahtumat.append(tapahtuma + "\n")

    def valinta(self, ehdokas: Ehdokas):
        pass

    def pudotus(self, ehdokas: Ehdokas):
        pass

    def uusi_kierros(self):
        pass

    def tulosta_tiedostoon(self, tiedosto):
        tiedosto.writelines(self.tapahtumat)
