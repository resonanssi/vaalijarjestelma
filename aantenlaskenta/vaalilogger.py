from ehdokas import Ehdokas
import utils


class VaaliLogger:
    tapahtumat: list[str]

    def __init__(self):
        self.tapahtumat = []

    def lisää_rivi(self, tapahtuma: str):
        self.tapahtumat.append(tapahtuma + "\n")

    def arvonnan_aloitus(self, ehdokkaat: list[Ehdokas]):
        ehdokas_nimet = [f"\t[{ehdokas._id}]: {ehdokas.nimi}" for ehdokas in ehdokkaat]
        tulostus = f"Arvotaan pudotettava ehdokkaista:\n" + "\n".join(ehdokas_nimet)
        self.lisää_rivi(tulostus)
        print(tulostus)

    def arvonnan_tulos(self, ehdokas: Ehdokas):
        tulostus = f"Pudotettiin ehdokas: [{ehdokas._id}] {ehdokas.nimi}"
        print(tulostus)
        self.lisää_rivi(tulostus)
        

    def nykytilanne(self, ehdokkaat: list[Ehdokas]):
        self.tapahtumat.append("\n".join(utils.nykytilanne(ehdokkaat)))

    def tulosta_tiedostoon(self, tiedosto):
        tiedosto.writelines(self.tapahtumat)


vaalilogger = VaaliLogger()
