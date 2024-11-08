from ehdokas import Ehdokas
from lipuke import Lipuke
import math


def etsi_ehdokas(ehdokkaat: list[Ehdokas], ehdokas_id: int) -> Ehdokas:
    for ehdokas in ehdokkaat:
        if ehdokas._id == ehdokas_id:
            return ehdokas

    raise Exception(f"Ehdokasta numero {ehdokas_id} ei löydy")


def laske_summat(ehdokkaat: list[Ehdokas], lipukkeet: list[Lipuke]) -> tuple[float, int]:

    äänihukka = 0.0
    hyväksytyt_äänet = 0

    for lipuke in lipukkeet:
        if len(lipuke.ehdokkaat) > 0:
            hyväksytyt_äänet += 1

        jäljellä = 1.0

        for ehdokas_id in lipuke.ehdokkaat:
            ehdokas = etsi_ehdokas(ehdokkaat, ehdokas_id) 
            ehdokas.summa += ehdokas.painokerroin * jäljellä
            jäljellä -= ehdokas.painokerroin * jäljellä

        äänihukka += jäljellä

    return (äänihukka, hyväksytyt_äänet)


def nollaa_summat(ehdokkaat: list[Ehdokas]):
    for ehdokas in ehdokkaat:
        ehdokas.summa = 0.0


def laske_äänikynnys(hyväksytyt_äänet: int, äänihukka: float, paikkamäärä: int) -> float:
    return (hyväksytyt_äänet - äänihukka) / paikkamäärä

def pyöristä_ylös_5_desimaalia(x: float) -> float:
    return math.ceil(x * 100_000) / 100_000
    

def suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet):

    nollaa_summat(ehdokkaat)
    äänihukka, hyväksytyt_äänet = laske_summat(ehdokkaat, lipukkeet)

    äänikynnys = laske_äänikynnys(hyväksytyt_äänet, äänihukka, paikkamäärä)

    for ehdokas in ehdokkaat:
        print(f"{ehdokas.nimi}: {ehdokas.summa}")

