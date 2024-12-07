from aantenlaskenta.ehdokas import Ehdokas, Tila
import math
import os


def ceil_5dec(x: float) -> float:
    return math.ceil(x * 100_000) / 100_000


def floor_5dec(x: float) -> float:
    return math.floor(x * 100_000) / 100_000


def etsi_ehdokkaat_tilassa(ehdokkaat: list[Ehdokas], tila: Tila) -> list[Ehdokas]:
    return [ehdokas for ehdokas in ehdokkaat if ehdokas.tila == tila]


def etsi_ehdokas(ehdokkaat: list[Ehdokas], ehdokas_id: int) -> Ehdokas | None:
    for ehdokas in ehdokkaat:
        if ehdokas._id == ehdokas_id:
            return ehdokas

    return None


def luo_lokihakemisto(hakemisto: str):
    if os.path.isdir(hakemisto):
        return

    os.makedirs(hakemisto)
    print(f"Luodaan lokeille hakemisto: {os.path.abspath(hakemisto)}")


def nykytilanne(ehdokkaat: list[Ehdokas]) -> list[str]:
    suurin_nimen_pituus = len("nimi")
    for ehdokas in ehdokkaat:
        suurin_nimen_pituus = max(len(ehdokas.nimi), suurin_nimen_pituus)

    id_pituus = 4
    id_teksti = "id".center(id_pituus, " ")

    nimi_pituus = suurin_nimen_pituus
    nimi_teksti = "nimi".center(nimi_pituus, " ")

    tila_pituus = len("Jättäytynyt")
    tila_teksti = "tila".center(tila_pituus, " ")

    painokerroin_pituus = 20
    painokerroin_teksti = "painokerroin".center(painokerroin_pituus, " ")

    ääniosuus_teksti = "ääniosuuksien summa"
    ääniosuus_pituus = len(ääniosuus_teksti)

    vaakaviivat = [
        "━" * pituus
        for pituus in [
            id_pituus,
            nimi_pituus,
            tila_pituus,
            painokerroin_pituus,
            ääniosuus_pituus,
        ]
    ]

    ylin_rivi = "┍━" + "━┯━".join(vaakaviivat) + "━┑"
    keskirivi = "┝━" + "━┿━".join(vaakaviivat) + "━┥"
    alin_rivi = "┕━" + "━┷━".join(vaakaviivat) + "━┙"

    tulostus = []
    tulostus.append(ylin_rivi)
    tulostus.append(
        "│ "
        + " │ ".join(
            [id_teksti, nimi_teksti, tila_teksti, painokerroin_teksti, ääniosuus_teksti]
        )
        + " │"
    )
    tulostus.append(keskirivi)

    for ehdokas in ehdokkaat:
        _id = str(ehdokas._id).center(id_pituus, " ")
        nimi = str(ehdokas.nimi).center(nimi_pituus, " ")
        tila = str(ehdokas.tila).center(tila_pituus, " ")
        painokerroin = str(ehdokas.painokerroin).center(painokerroin_pituus, " ")
        summa = str(floor_5dec(ehdokas.summa)).center(ääniosuus_pituus, " ")
        tulostus.append(
            "│ " + " │ ".join([_id, nimi, tila, painokerroin, summa]) + " │"
        )

    tulostus.append(alin_rivi)

    return tulostus


class VaaliException(Exception):
    pass
