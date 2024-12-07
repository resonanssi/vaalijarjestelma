import aantenlaskenta.pudotus as pudotus
from aantenlaskenta.ehdokas import Ehdokas
from aantenlaskenta.lipuke import Lipuke


def luo_testiehdokkaat(*nimet: list[str]) -> list[Ehdokas]:
    return [Ehdokas(x, i + 1) for (i, x) in enumerate(nimet)]


def luo_lipukkeet(*lipukkeet) -> list[Lipuke]:
    return [Lipuke(lipuke) for lipuke in lipukkeet]


def test_etsi_pienimmät():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    for ehdokas, summa in zip(ehdokkaat, [1.0, 2.0, 2.0, 4.0]):
        ehdokas.summa = summa

    pienimmät = pudotus.etsi_pienimmät(ehdokkaat)
    assert pienimmät == [ehdokkaat[0]]

    ehdokkaat[0].summa = 100.0
    pienimmät = pudotus.etsi_pienimmät(ehdokkaat)
    assert pienimmät == [ehdokkaat[1], ehdokkaat[2]]


def test_arvonta_palauttaa_yhden():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D", "E")

    valittu = pudotus.arvo_pudotettava(ehdokkaat)
    assert valittu in ehdokkaat


def test_vertaile_pienimpiä1():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    lipukkeet = luo_lipukkeet([1, 2, 3, 4], [1, 2, 3, 4])

    pienimmät = pudotus.vertaile_pienimpiä(ehdokkaat, lipukkeet)
    assert pienimmät == [ehdokkaat[3]]


def test_vertaile_pienimpiä2():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    lipukkeet = luo_lipukkeet([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 4, 3], [1, 2, 4, 3])

    pienimmät = pudotus.vertaile_pienimpiä(ehdokkaat, lipukkeet)
    assert pienimmät == [ehdokkaat[2], ehdokkaat[3]]


def test_vertaile_pienimpiä3():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    lipukkeet = luo_lipukkeet([1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3])

    pienimmät = pudotus.vertaile_pienimpiä(ehdokkaat, lipukkeet)
    assert pienimmät == ehdokkaat
