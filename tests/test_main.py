from main import poista_jättäytyneet_lipukkeista
from ehdokas import Ehdokas, Tila
from lipuke import Lipuke


def alusta_ehdokkaat():
    return [
        Ehdokas("Ehdokas 1", 1),
        Ehdokas("Ehdokas 2", 2),
        Ehdokas("Ehdokas 3", 3),
        Ehdokas("Ehdokas 4", 4),
        Ehdokas("Ehdokas 5", 5),
    ]


def alusta_lipukkeet():
    return [
        Lipuke([1, 2, 3, 4, 5]),
        Lipuke([5, 4, 3, 2, 1]),
        Lipuke([1, 3, 5]),
        Lipuke([2, 4]),
    ]


def test_jättäytyminen1():
    ehdokkaat = alusta_ehdokkaat()
    lipukkeet = alusta_lipukkeet()

    poista_jättäytyneet_lipukkeista([ehdokkaat[0], ehdokkaat[1]], lipukkeet)

    assert ehdokkaat[0].tila == Tila.Jättäytynyt
    assert ehdokkaat[1].tila == Tila.Jättäytynyt

    assert ehdokkaat[2].tila == Tila.Toiveikas
    assert ehdokkaat[3].tila == Tila.Toiveikas
    assert ehdokkaat[4].tila == Tila.Toiveikas

    assert lipukkeet[0].ehdokkaat == [3, 4, 5]
    assert lipukkeet[1].ehdokkaat == [5, 4, 3]
    assert lipukkeet[2].ehdokkaat == [3, 5]
    assert lipukkeet[3].ehdokkaat == [4]


def test_jättäytyminen2():
    ehdokkaat = alusta_ehdokkaat()
    lipukkeet = alusta_lipukkeet()

    poista_jättäytyneet_lipukkeista(
        [ehdokkaat[0], ehdokkaat[2], ehdokkaat[4]], lipukkeet
    )

    assert ehdokkaat[0].tila == Tila.Jättäytynyt
    assert ehdokkaat[2].tila == Tila.Jättäytynyt
    assert ehdokkaat[4].tila == Tila.Jättäytynyt

    assert ehdokkaat[1].tila == Tila.Toiveikas
    assert ehdokkaat[3].tila == Tila.Toiveikas

    assert lipukkeet[0].ehdokkaat == [2, 4]
    assert lipukkeet[1].ehdokkaat == [4, 2]
    assert lipukkeet[2].ehdokkaat == []
    assert lipukkeet[3].ehdokkaat == [2, 4]
