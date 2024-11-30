from ehdokas import Ehdokas
import utils


class VaaliLogger:
    tapahtumat: list[str]

    def __init__(self):
        self.tapahtumat = []

    def lisää_rivi(self, tapahtuma: str):
        self.tapahtumat.append(tapahtuma + "\n")

    def nykytilanne(self, ehdokkaat: list[Ehdokas]):
        self.tapahtumat.append("\n".join(utils.nykytilanne(ehdokkaat)))

    def tulosta_tiedostoon(self, tiedosto):
        tiedosto.writelines(self.tapahtumat)
