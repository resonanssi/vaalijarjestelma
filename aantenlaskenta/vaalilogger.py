from ehdokas import Ehdokas
import utils


class VaaliLogger:
    tapahtumat: list[str]

    def __init__(self):
        self.tapahtumat = []

    def lisää_rivi(self, tapahtuma: str, vain_tiedostoon=False):
        print(tapahtuma)
        self.tapahtumat.append(tapahtuma + "\n")

    def arvonnan_aloitus(self, ehdokkaat: list[Ehdokas]):
        ehdokas_nimet = [f"\t[{ehdokas._id}]: {ehdokas.nimi}" for ehdokas in ehdokkaat]
        tulostus = f"Arvotaan pudotettava ehdokkaista:\n" + "\n".join(ehdokas_nimet)
        self.lisää_rivi(tulostus)

    def arvonnan_tulos(self, ehdokas: Ehdokas):
        tulostus = f"Pudotettiin ehdokas: [{ehdokas._id}] {ehdokas.nimi}"
        self.lisää_rivi(tulostus)

    def uusi_kierros(self, kierros_nro: int):
        tulostus = f"{"-"*80}\n Kierros {kierros_nro}\n"
        self.lisää_rivi(tulostus)

    def nykytilanne(self, ehdokkaat: list[Ehdokas], vain_tiedostoon=False):
        tulostus = "\n".join(utils.nykytilanne(ehdokkaat))
        self.lisää_rivi(tulostus, vain_tiedostoon)

    def tulosta_tiedostoon(self, tiedosto):
        tiedosto.writelines(self.tapahtumat)


vaalilogger = VaaliLogger()
