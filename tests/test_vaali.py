import aantenlaskenta.vaali as vaali
from aantenlaskenta.ehdokas import Ehdokas, Tila
from aantenlaskenta.lipuke import Lipuke
from aantenlaskenta.utils import etsi_ehdokkaat_tilassa, etsi_ehdokas


def luo_testiehdokkaat(määrä: int, *nimet: list[str]) -> list[Ehdokas]:
    return [Ehdokas(f"Ehdokas {i}", i) for i in range(1, määrä + 1)]


def luo_lipukkeet(*lipukkeet) -> list[Lipuke]:
    return [Lipuke(lipuke) for lipuke in lipukkeet]


def test_nollaa_summat():
    ehdokkaat = luo_testiehdokkaat(4)
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
    ehdokkaat = luo_testiehdokkaat(4)
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
    ehdokas = luo_testiehdokkaat(1)[0]
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
    ehdokkaat = luo_testiehdokkaat(4)
    äänikynnys = 3.00002
    for ehdokas in ehdokkaat:
        ehdokas.tila = Tila.Valittu
        ehdokas.summa = 3.00003

    assert vaali.valittujen_summat_oikein(ehdokkaat, äänikynnys)

    ehdokkaat[3].summa = 3.0000

    assert not vaali.valittujen_summat_oikein(ehdokkaat, äänikynnys)


def test_valitse_toiveikkaat():
    ehdokkaat = luo_testiehdokkaat(4)
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


def test_monta_kierrosta():
    paikkamäärä = 4
    ehdokkaat = luo_testiehdokkaat(10)
    lipukkeet = luo_lipukkeet(
        [7, 2, 3, 4, 5, 8, 1, 6, 9, 10],
        [1, 6, 7, 4, 9, 3, 8, 2, 5, 10],
        [6, 3, 9, 7, 1, 8, 2, 4, 5],
        [6, 4, 5, 2, 9, 1, 8, 7, 3],
        [3, 4, 9, 8, 1, 2, 5, 6, 7],
        [5, 4, 2, 9, 6, 3, 8, 1, 7],
        [2, 4, 5, 7, 6, 9, 1, 8, 3],
        [9, 2, 5, 8, 3, 7, 6, 1, 4],
        [5, 8, 3, 4, 7, 2, 6, 9, 1],
        [7, 3, 8, 1, 9, 5, 6, 2, 4],
        [5, 7, 3, 2, 8, 9, 4, 6, 1],
        [1, 6, 3, 5, 4, 2, 7, 8, 9],
        [7, 9, 2, 6, 8, 5, 4, 1, 3],
        [9, 8, 5, 7, 6, 4, 3, 2, 1],
        [8, 7, 6, 4, 5, 9, 3, 1, 2],
    )

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokas(ehdokkaat, 10).tila == Tila.Pudotettu

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokas(ehdokkaat, 4).tila == Tila.Pudotettu

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokas(ehdokkaat, 8).tila == Tila.Pudotettu

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, 7)
    ]

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokas(ehdokkaat, 2).tila == Tila.Pudotettu

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, 5),
        etsi_ehdokas(ehdokkaat, 7)
    ]

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokas(ehdokkaat, 3).tila == Tila.Pudotettu

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokas(ehdokkaat, 1).tila == Tila.Pudotettu

    vaali.kierros(paikkamäärä, ehdokkaat, lipukkeet)
    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, 5),
        etsi_ehdokas(ehdokkaat, 6),
        etsi_ehdokas(ehdokkaat, 7),
        etsi_ehdokas(ehdokkaat, 9)
    ]
