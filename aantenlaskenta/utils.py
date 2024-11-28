from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
import math

def ceil_5dec(x: float) -> float:
    return math.ceil(x * 100_000) / 100_000


def floor_5dec(x: float) -> float:
    return math.floor(x * 100_000) / 100_000


def etsi_ehdokkaat_tilassa(ehdokkaat: list[Ehdokas], tila: Tila) -> list[Ehdokas]:
    return [ehdokas for ehdokas in ehdokkaat if ehdokas.tila == tila]


def etsi_ehdokas(ehdokkaat: list[Ehdokas], ehdokas_id: int) -> Ehdokas:
    for ehdokas in ehdokkaat:
        if ehdokas._id == ehdokas_id:
            return ehdokas

    raise Exception(f"Ehdokasta numero {ehdokas_id} ei löydy")
