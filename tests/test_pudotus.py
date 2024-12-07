from aantenlaskenta.pudotus import etsi_pienimmät
from aantenlaskenta.ehdokas import Ehdokas, Tila


def luo_testiehdokkaat(*nimet: list[str]) -> list[Ehdokas]:
    return [Ehdokas(x, i) for (i, x) in enumerate(nimet)]


def test_etsi_pienimmät():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    for ehdokas, summa in zip(ehdokkaat, [1.0, 2.0, 2.0, 4.0]):
        ehdokas.summa = summa

    pienimmät = etsi_pienimmät(ehdokkaat)
    assert pienimmät == [ehdokkaat[0]]

    ehdokkaat[0].summa = 100.0
    pienimmät = etsi_pienimmät(ehdokkaat)
    assert pienimmät == [ehdokkaat[1], ehdokkaat[2]]
