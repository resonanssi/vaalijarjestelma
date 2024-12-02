import vaali
from ehdokas import Ehdokas, Tila


def luo_testiehdokkaat(*nimet: list[str]) -> list[Ehdokas]:
    return [Ehdokas(x, i) for (i, x) in enumerate(nimet)]


def test_nollaa_summat():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    ehdokkaat[0].summa = 1.0
    ehdokkaat[1].summa = 2.0
    ehdokkaat[2].summa = 3.0
    ehdokkaat[3].summa = 4.0

    vaali.nollaa_summat(ehdokkaat)

    for ehdokas in ehdokkaat:
        assert ehdokas.summa == 0.0


def test_äänikynnys1():
    hyväksytyt_äänet = 100
    äänihukka = 12.4
    paikkamäärä = 24

    äänikynnys = vaali.laske_äänikynnys(hyväksytyt_äänet, äänihukka, paikkamäärä)

    assert äänikynnys == 3.65


def test_äänikynnys2():
    hyväksytyt_äänet = 10
    äänihukka = 0.0
    paikkamäärä = 3

    äänikynnys = vaali.laske_äänikynnys(hyväksytyt_äänet, äänihukka, paikkamäärä)

    assert äänikynnys == 3.33334


def test_painokertoimet():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    painokertoimet = [1.0, 0.5, 0.9, 0.2]
    summat = [10.6, 3.9, 14.0, 6.5]

    for ehdokas, pk, summa in zip(ehdokkaat, painokertoimet, summat):
        ehdokas.tila = Tila.Valittu
        ehdokas.painokerroin = pk
        ehdokas.summa = summa

    äänikynnys = 4.0
    vaali.päivitä_painokertoimet(ehdokkaat, äänikynnys)

    oikeat_painokertoimet = [
        0.37735849056603776,
        0.5128205128205129,
        0.2571428571428571,
        0.12307692307692308,
    ]

    for ehdokas, oikea_pk in zip(ehdokkaat, oikeat_painokertoimet):
        assert ehdokas.painokerroin == oikea_pk


def test_valituilla_oikeat_summat1():
    ehdokas = luo_testiehdokkaat("A")[0]
    ehdokas.tila = Tila.Valittu
    äänikynnys = 2.00002

    ehdokas.summa = 1.0
    assert not vaali.valittujen_summat_oikein([ehdokas], äänikynnys)

    ehdokas.summa = 2.0
    assert not vaali.valittujen_summat_oikein([ehdokas], äänikynnys)

    ehdokas.summa = 2.00001
    assert vaali.valittujen_summat_oikein([ehdokas], äänikynnys)

    ehdokas.summa = 2.00002
    assert vaali.valittujen_summat_oikein([ehdokas], äänikynnys)

    ehdokas.summa = 2.00003
    assert vaali.valittujen_summat_oikein([ehdokas], äänikynnys)

    ehdokas.summa = 2.00004
    assert not vaali.valittujen_summat_oikein([ehdokas], äänikynnys)


def test_valituilla_oikeat_summat2():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    äänikynnys = 3.00002
    for ehdokas in ehdokkaat:
        ehdokas.tila = Tila.Valittu
        ehdokas.summa = 3.00003

    assert vaali.valittujen_summat_oikein(ehdokkaat, äänikynnys)

    ehdokkaat[3].summa = 3.0000

    assert not vaali.valittujen_summat_oikein(ehdokkaat, äänikynnys)


def test_valitse_toiveikkaat():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    äänikynnys = 3.50001
    summat = [1.0, 3.5, 3.50002, 3.6]
    for ehdokas, summa in zip(ehdokkaat, summat):
        ehdokas.summa = summa

    valitut = vaali.valitse_toiveikkaat(ehdokkaat, äänikynnys)

    assert valitut == [ehdokkaat[2], ehdokkaat[3]]

    assert ehdokkaat[0].tila == Tila.Toiveikas
    assert ehdokkaat[1].tila == Tila.Toiveikas
    assert ehdokkaat[2].tila == Tila.Valittu
    assert ehdokkaat[3].tila == Tila.Valittu


def test_pudota_pienin():
    ehdokkaat = luo_testiehdokkaat("A", "B", "C", "D")
    for ehdokas, summa in zip(ehdokkaat, [1.0, 2.0, 3.0, 4.0]):
        ehdokas.summa = summa

    pudotettu = vaali.pudota_pienin(ehdokkaat)
    assert pudotettu == ehdokkaat[0]

    ehdokkaat[0].summa = 100.0
    pudotettu = vaali.pudota_pienin(ehdokkaat)
    assert pudotettu == ehdokkaat[1]
