from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
from utils import ceil_5dec, etsi_ehdokas, etsi_ehdokkaat_tilassa, VaaliException
from laske_summat import laske_summat
from vaalilogger import vaalilogger
import secrets


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


def arvo_pudotettava(pienimmät: list[Ehdokas]) -> Ehdokas:
    valittu = secrets.choice(pienimmät)
    return valittu


def etsi_pienimmät(toiveikkaat: list[Ehdokas], pudotusvertailu=False) -> list[Ehdokas]:
    if pudotusvertailu:
        pienin_summa = min(
            map(lambda ehdokas: ehdokas.pudotusvertailu_summa, toiveikkaat)
        )
        pienimmät = [
            ehdokas
            for ehdokas in toiveikkaat
            if ehdokas.pudotusvertailu_summa == pienin_summa
        ]
    else:
        pienin_summa = min(map(lambda ehdokas: ehdokas.summa, toiveikkaat))
        pienimmät = [
            ehdokas for ehdokas in toiveikkaat if ehdokas.summa == pienin_summa
        ]

    vaalilogger.lisää_rivi(f"Pienin summa: {pienin_summa}", vain_tiedostoon=True)
    vaalilogger.lisää_rivi("Pienimmän summan omaavat ehdokkaat:", vain_tiedostoon=True)

    for ehdokas in pienimmät:
        vaalilogger.lisää_rivi(f"\t{ehdokas}", vain_tiedostoon=True)
    return pienimmät


def vertaile_pienimpiä(
    pienimmät: list[Ehdokas], lipukkeet: list[Lipuke]
) -> list[Ehdokas]:
    vanhat_pienimmät = None
    while True:
        for ehdokas in pienimmät:
            ehdokas.pudotusvertailu_summa = 0.0
        for lipuke in lipukkeet:
            for ehdokas_id in lipuke.ehdokkaat:
                ehdokas = etsi_ehdokas(pienimmät, ehdokas_id)
                if ehdokas is not None:
                    ehdokas.pudotusvertailu_summa += 1.0
                    break

        vanhat_pienimmät = pienimmät
        pienimmät = etsi_pienimmät(pienimmät, pudotusvertailu=True)
        if len(pienimmät) == 1 or pienimmät == vanhat_pienimmät:
            return pienimmät


def suorita_pudotus(ehdokkaat: list[Ehdokas], lipukkeet: list[Lipuke]):
    vaalilogger.lisää_rivi("Kierroksella ei valittu ketään. Aloitetaan pudotus.\n")
    toiveikkaat = etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Toiveikas)
    pienimmät = etsi_pienimmät(toiveikkaat)

    if len(pienimmät) == 0:
        raise VaaliException("ei löytynyt pienimmän summan ehdokkaita.")
    if len(pienimmät) == 1:
        pienimmät[0].pudota()
        return

    pienimmät = vertaile_pienimpiä(pienimmät, lipukkeet)

    if len(pienimmät) == 0:
        raise VaaliException("vertailun jälkeen ei löytynyt pudotettavia.")
    if len(pienimmät) == 1:
        pienimmät[0].pudota()
        return

    vaalilogger.arvonnan_aloitus(pienimmät)
    pudotettava = arvo_pudotettava(pienimmät)
    vaalilogger.lisää_rivi(f"Arvonnalla valittiin pudotettavaksi {pudotettava}")
    pudotettava.pudota()


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
        for toiveikas in toiveikkaat:
            toiveikas.tila = Tila.Valittu

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
        vaalilogger.nykytilanne(ehdokkaat)
        kierros_nro += 1
