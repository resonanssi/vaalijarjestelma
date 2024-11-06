from ääntenlaskenta.main import lue_lipukkeet
import pytest

def test_tyhjä_syöte_antaa_virheen():
    syöte = ""
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
