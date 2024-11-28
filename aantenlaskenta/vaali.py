from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
from utils import ceil_5dec, etsi_ehdokkaat_tilassa
from laske_summat import laske_summat


def nollaa_summat(ehdokkaat: list[Ehdokas]):
    for ehdokas in ehdokkaat:
        ehdokas.summa = 0.0


def laske_äänikynnys(
    hyväksytyt_äänet: int, äänihukka: float, paikkamäärä: int
) -> float:
    return ceil_5dec((hyväksytyt_äänet - äänihukka) / paikkamäärä)


def päivitä_painokertoimet(ehdokkaat: list[Ehdokas], äänikynnys: int) -> bool:
    print("Äänikynnys:", äänikynnys)
    for ehdokas in ehdokkaat:
        if ehdokas.tila != Tila.Valittu:
            continue

        print(f"Ehdokas {ehdokas.nimi}, summa: {ehdokas.summa}")

        vanha = ehdokas.painokerroin
        ehdokas.painokerroin *= äänikynnys / ehdokas.summa


def valittujen_painokertoimet_oikein(ehdokkaat: list[Ehdokas], äänikynnys: int) -> bool:
    for ehdokas in ehdokkaat:
        if ehdokas.tila == Tila.Valittu and abs(ehdokas.summa - äänikynnys) > 0.00001:
            return False

    return True


def valitse_toiveikkaat(toiveikkaat: list[Ehdokas], äänikynnys) -> list[Ehdokas]:
    valitut = []
    for ehdokas in toiveikkaat:
        assert ehdokas.tila == Tila.Toiveikas
        if ehdokas.summa >= äänikynnys:
            print(f"Valitaan ehdokas [{ehdokas._id}]: {ehdokas.nimi}")
            ehdokas.valitse()
            valitut.append(ehdokas)

    return valitut


def arvo_pudotettava(pienimmät: list[Ehdokas]) -> Ehdokas:
    pienimmät[0].pudota()  # TODO arvo oikeasti
    return pienimmät[0]


def pudota_pienin(toiveikkaat: list[Ehdokas]) -> Ehdokas | None:
    pienin_summa = min(map(lambda ehdokas: ehdokas.summa, toiveikkaat))
    pienimmät = [ehdokas for ehdokas in toiveikkaat if ehdokas.summa == pienin_summa]

    if len(pienimmät) == 1:
        pienimmät[0].tila = Tila.Pudotettu

        return pienimmät[0]

    pudotettu = arvo_pudotettava(pienimmät)
    return pudotettu


def kierros(paikkamäärä, ehdokkaat, lipukkeet):
    jatketaan = True

    while jatketaan:
        nollaa_summat(ehdokkaat)

        äänihukka, hyväksytyt_äänet = laske_summat(ehdokkaat, lipukkeet)

        äänikynnys = laske_äänikynnys(hyväksytyt_äänet, äänihukka, paikkamäärä)

        päivitä_painokertoimet(ehdokkaat, äänikynnys)
        jatketaan = not valittujen_painokertoimet_oikein(ehdokkaat, äänikynnys)

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

    pudotettu = pudota_pienin(toiveikkaat)

    if pudotettu is not None:
        print(f"Pudotetaan ehdokas [{pudotettu._id}]: {pudotettu.nimi}")
        return


def suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet):
    print(f"Paikkoja: {paikkamäärä}\nehdokkaita: {len(ehdokkaat)}")
    while True:
        valitut = etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu)
        print(f"valittuja: {len(valitut)}")
        if len(valitut) == paikkamäärä:
            break

        kierros(paikkamäärä, ehdokkaat, lipukkeet)
        print()

    for ehdokas in ehdokkaat:
        print(f"{ehdokas.nimi}: {ehdokas.summa}, {ehdokas.tila}")
