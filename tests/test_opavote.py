from aantenlaskenta.opavote import lue_lipukkeet
import pytest


def test_tyhjä_syöte_antaa_virheen():
    syöte = ""
    with pytest.raises(StopIteration):
        lue_lipukkeet(syöte)


def test_nimen_puuttuminen_antaa_virheen():
    syöte = """
        2 1
        1 1 2 0
        0
        "Ehdokas 1"
        "Ehdokas 2"
    """.strip().split("\n")

    with pytest.raises(StopIteration):
        lue_lipukkeet(syöte)


def test_lyhyt_syöte():
    syöte = """
        2 1
        1 1 2 0
        0
        "Ehdokas 1"
        "Ehdokas 2"
        "Testivaali"
    """.strip().split("\n")

    vaalin_nimi, valittavien_määrä, ehdokkaat, lipukkeet = lue_lipukkeet(syöte)

    assert vaalin_nimi == "Testivaali"
    assert valittavien_määrä == 1
    assert len(ehdokkaat) == 2
    assert ehdokkaat[0].nimi == "Ehdokas 1"
    assert ehdokkaat[1].nimi == "Ehdokas 2"
    assert len(lipukkeet) == 1
    assert lipukkeet[0].ehdokkaat == [1, 2]


def test_pitkä_vaali():
    syöte = """
        10 5
        1 6 3 7 1 8 4 5 2 0
        1 8 5 2 9 7 1 4 0
        1 9 0
        1 9 2 5 10 7 8 3 1 6 0
        1 4 3 1 9 2 7 6 8 5 10 0
        1 2 1 7 6 9 8 0
        1 7 5 9 0
        1 4 3 5 8 10 2 6 9 1 7 0
        1 3 4 9 6 8 10 5 1 2 7 0
        1 1 2 9 3 7 5 6 10 4 8 0
        1 4 10 1 6 0
        1 3 6 8 7 5 4 10 9 1 2 0
        1 3 10 8 7 1 9 5 4 0
        1 4 2 10 9 5 3 6 0
        1 1 7 8 3 9 5 4 2 10 6 0
        1 2 9 4 1 8 10 5 7 6 3 0
        1 3 5 8 4 9 6 7 10 2 1 0
        1 3 1 2 4 9 6 7 5 8 0
        1 4 8 5 1 2 3 10 6 9 7 0
        1 3 2 8 5 7 4 9 0
        1 3 9 7 6 5 10 4 8 1 2 0
        1 5 3 1 9 2 6 10 8 4 7 0
        1 6 3 2 7 1 10 8 9 5 4 0
        1 3 9 10 5 0
        1 1 6 5 10 8 7 4 0
        0
        "Candidate 1"
        "Candidate 2"
        "Candidate 3"
        "Candidate 4"
        "Candidate 5"
        "Candidate 6"
        "Candidate 7"
        "Candidate 8"
        "Candidate 9"
        "Candidate 10"
        "Testivaali"    
    """.strip().split("\n")

    vaalin_nimi, valittavien_määrä, ehdokkaat, lipukkeet = lue_lipukkeet(syöte)

    assert vaalin_nimi == "Testivaali"
    assert valittavien_määrä == 5
    assert len(ehdokkaat) == 10
    assert len(lipukkeet) == 25
