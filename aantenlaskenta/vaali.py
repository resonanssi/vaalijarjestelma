from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
from utils import ceil_5dec, etsi_ehdokas, etsi_ehdokkaat_tilassa, VaaliException
from laske_summat import laske_summat
from vaalilogger import vaalilogger
from pudotus import suorita_pudotus


def nollaa_summat(ehdokkaat: list[Ehdokas]):
    for ehdokas in ehdokkaat:
        ehdokas.summa = 0.0


def laske_äänikynnys(
    hyväksytyt_äänet: int, äänihukka: float, paikkamäärä: int
) -> float:
    return ceil_5dec((hyväksytyt_äänet - äänihukka) / paikkamäärä)


def päivitä_painokertoimet(ehdokkaat: list[Ehdokas], äänikynnys: float):
    for ehdokas in ehdokkaat:
        if ehdokas.tila != Tila.Valittu:
            continue

        ehdokas.painokerroin *= äänikynnys / ehdokas.summa


def valittujen_summat_oikein(ehdokkaat: list[Ehdokas], äänikynnys: float) -> bool:
    for ehdokas in ehdokkaat:
        if not ehdokas.tila == Tila.Valittu:
            continue

        if round(100_000 * abs(ehdokas.summa - äänikynnys)) > 1:
            return False

    return True


def valitse_toiveikkaat(toiveikkaat: list[Ehdokas], äänikynnys) -> list[Ehdokas]:
    valitut = []
    for ehdokas in toiveikkaat:
        assert ehdokas.tila == Tila.Toiveikas
        if ehdokas.summa >= äänikynnys:
            print(f"Valitaan ehdokas {ehdokas}")
            ehdokas.valitse()
            valitut.append(ehdokas)

    return valitut


def kierros(paikkamäärä, ehdokkaat, lipukkeet):
    jatketaan = True
    äänikynnys = float("inf")

    while jatketaan:
        for ehdokas in ehdokkaat:
            ehdokas.alusta_painokerroin()

        nollaa_summat(ehdokkaat)

        äänihukka, hyväksytyt_äänet = laske_summat(ehdokkaat, lipukkeet)

        äänikynnys = laske_äänikynnys(hyväksytyt_äänet, äänihukka, paikkamäärä)

        päivitä_painokertoimet(ehdokkaat, äänikynnys)
        jatketaan = not valittujen_summat_oikein(ehdokkaat, äänikynnys)

    valitut = etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu)
    toiveikkaat = etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Toiveikas)

    if len(valitut) + len(toiveikkaat) == paikkamäärä:
        # valitaan loput
        vaalilogger.lisää_rivi("Valitaan loput ehdokkaat:")
        for toiveikas in toiveikkaat:
            toiveikas.tila = Tila.Valittu
            vaalilogger.lisää_rivi(f"\t{toiveikas}")

        return

    valitut = valitse_toiveikkaat(toiveikkaat, äänikynnys)

    if len(valitut) > 0:
        return

    suorita_pudotus(ehdokkaat, lipukkeet)


def suorita_vaali(paikkamäärä: int, ehdokkaat: list[Ehdokas], lipukkeet: list[Lipuke]):
    vaalilogger.lisää_rivi(f"Paikkoja: {paikkamäärä}\nehdokkaita: {len(ehdokkaat)}")
    kierros_nro = 1
    while True:
        valitut = etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu)
        if len(valitut) == paikkamäärä:
            break

        vaalilogger.uusi_kierros(kierros_nro)
        kierros(paikkamäärä, ehdokkaat, lipukkeet)
        vaalilogger.lisää_rivi("\nTilanne kierroksen lopussa:")
        vaalilogger.nykytilanne(ehdokkaat)
        kierros_nro += 1
