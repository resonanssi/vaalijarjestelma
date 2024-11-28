from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
from utils import floor_5dec, etsi_ehdokas

def laske_summat(ehdokkaat: list[Ehdokas], lipukkeet: list[Lipuke]) -> tuple[float, int]:
    äänihukka = 0.0
    hyväksytyt_äänet = 0

    for lipuke in lipukkeet:
        if len(lipuke.ehdokkaat) > 0:
            hyväksytyt_äänet += 1

        jäljellä = 1.0

        for ehdokas_id in lipuke.ehdokkaat:
            ehdokas = etsi_ehdokas(ehdokkaat, ehdokas_id) 
            muutos = ehdokas.painokerroin * jäljellä
            ehdokas.summa += muutos
            jäljellä -= muutos

        äänihukka += jäljellä

    for ehdokas in ehdokkaat:
        ehdokas.summa = floor_5dec(ehdokas.summa)

    return (äänihukka, hyväksytyt_äänet)

