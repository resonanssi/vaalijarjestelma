import vaali
from ehdokas import Ehdokas, Tila
from lipuke import Lipuke


def luo_ehdokkaat(nimet: list[str]):
    return [Ehdokas(nimi, i) for (i, nimi) in enumerate(nimet)]


def luo_lipukkeet(äänet: list[list[int]]):
    lipukkeet = []
    for lipuke in äänet:
        lipukkeet.append(Lipuke(lipuke))

    return lipukkeet


def test_summat_kaikki_toiveikkaita():
    nimet = ["A", "B", "C", "D", "E", "F"]
    äänet = [[0, 1, 2, 3, 4, 5], [2, 1], [2], [3, 2, 5], [3, 4, 2], [3, 5, 1]]

    ehdokkaat = luo_ehdokkaat(nimet)
    lipukkeet = luo_lipukkeet(äänet)

    vaali.laske_summat(ehdokkaat, lipukkeet)

    assert ehdokkaat[0].summa == 1
    assert ehdokkaat[1].summa == 0
    assert ehdokkaat[2].summa == 2
    assert ehdokkaat[3].summa == 3
    assert ehdokkaat[4].summa == 0
    assert ehdokkaat[5].summa == 0


def test_summat_pudotettuja():
    nimet = ["A", "B", "C", "D", "E", "F"]
    äänet = [[0, 1, 2, 3, 4, 5], [2, 1], [2], [3, 2, 5], [3, 4, 2], [3, 5, 1]]

    ehdokkaat = luo_ehdokkaat(nimet)
    lipukkeet = luo_lipukkeet(äänet)

    ehdokkaat[3].pudota()
    ehdokkaat[5].pudota()

    vaali.laske_summat(ehdokkaat, lipukkeet)

    assert ehdokkaat[0].summa == 1
    assert ehdokkaat[1].summa == 1
    assert ehdokkaat[2].summa == 3
    assert ehdokkaat[3].summa == 0
    assert ehdokkaat[4].summa == 1
    assert ehdokkaat[5].summa == 0
