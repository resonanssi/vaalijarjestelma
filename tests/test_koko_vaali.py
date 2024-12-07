from aantenlaskenta.opavote import lue_lipukkeet
from aantenlaskenta.ehdokas import Tila
from aantenlaskenta.vaali import suorita_vaali
from aantenlaskenta.utils import etsi_ehdokkaat_tilassa, etsi_ehdokas


# Näissä testeissä käytetyt vaalitiedostot ovat oikeita
# vaaleja vuodelta 2023, mutta niistä on nimet poistettu

def test_hallitusvaali():
    with open("testivaaleja/hallitusvaali.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_lipukkeet(f.readlines())

    assert vaalin_nimi == "hallitusvaali"
    assert paikkamäärä == 11
    assert len(ehdokkaat) == 15
    assert len(lipukkeet) == 65

    suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet)

    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, ehdokas_id)
        for ehdokas_id in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13]
    ]


def test_virkailijavaali():
    with open("testivaaleja/virkailijavaali1.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_lipukkeet(f.readlines())

    assert vaalin_nimi == "virkailijavaali"
    assert paikkamäärä == 1
    assert len(ehdokkaat) == 2
    assert len(lipukkeet) == 69

    suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet)

    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, 2)
    ]


def test_virkailijavaali2():
    with open("testivaaleja/virkailijavaali2.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_lipukkeet(f.readlines())

    assert vaalin_nimi == "virkailijavaali"
    assert paikkamäärä == 1
    assert len(ehdokkaat) == 2
    assert len(lipukkeet) == 66

    suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet)

    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, 2)
    ]


def test_virkailijavaali3():
    with open("testivaaleja/virkailijavaali3.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_lipukkeet(f.readlines())

    assert vaalin_nimi == "virkailijavaali"
    assert paikkamäärä == 1
    assert len(ehdokkaat) == 2
    assert len(lipukkeet) == 69

    suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet)

    assert etsi_ehdokkaat_tilassa(ehdokkaat, Tila.Valittu) == [
        etsi_ehdokas(ehdokkaat, 2)
    ]
