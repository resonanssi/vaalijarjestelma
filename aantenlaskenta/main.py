from aantenlaskenta.opavote import lue_lipukkeet
from aantenlaskenta.ehdokas import Ehdokas, Tila
from aantenlaskenta.lipuke import Lipuke
from aantenlaskenta.vaali import suorita_vaali
from aantenlaskenta.vaalilogger import vaalilogger
from aantenlaskenta.utils import luo_lokihakemisto, VaaliException
from datetime import datetime
import os
import sys


def kysy_jättäytyneet(ehdokkaat: list[Ehdokas]):
    print("Kuka/ketkä ehdokkaista jättäytyvät?\n")

    for ehdokas in ehdokkaat:
        print(f"[{ehdokas._id}]: {ehdokas.nimi}")

    print("\nSyötä pois jättäytyvän ehdokkaan id (nimeä edeltävä numero).")
    print(
        "Jos pois jättäytyviä ehdokkaita on monta, syötä ne kaikki pilkulla erotettuna."
    )
    print("Esimerkiksi: 2, 3, 10\n")

    syöte = input("> ").strip().split(",")
    try:
        pois_jättäytyvät_id = [int(id) for id in syöte]
    except ValueError:
        raise VaaliException("Kirjoita syöte oikeassa muodossa!")

    pois_jättäytyvät = []

    for id in pois_jättäytyvät_id:
        filtteröidyt = list(filter(lambda ehdokas: ehdokas._id == id, ehdokkaat))

        if len(filtteröidyt) == 0:
            raise VaaliException(f"Ehdokasta numero {id} ei löytynyt!")

        ehdokas = filtteröidyt[0]
        print(f"Merkitään ehdokas {ehdokas.nimi} jättäytyneeksi pois")
        pois_jättäytyvät.append(ehdokas)

    return pois_jättäytyvät


def poista_jättäytyneet_lipukkeista(
    jättäytyneet: list[Ehdokas], lipukkeet: list[Lipuke]
):
    for ehdokas in jättäytyneet:
        ehdokas.tila = Tila.Jättäytynyt
        ehdokas.painokerroin = 0.0

    jättäytyneet_id = [ehdokas._id for ehdokas in jättäytyneet]

    for lipuke in lipukkeet:
        lipuke.ehdokkaat = [id for id in lipuke.ehdokkaat if id not in jättäytyneet_id]


def lue_vaalitiedosto(tiedosto: str) -> (str, int, list[Ehdokas], list[Lipuke]):
    with open(tiedosto) as f:
        return lue_lipukkeet(f.readlines())


def main():
    # vaalitiedoston nimen voi syöttää parametrina
    # esim. python aantenlaskenta/main.py testivaali.txt
    if len(sys.argv) > 1:
        vaalitiedosto = sys.argv[1]
    else:
        print("Syötä vaalitiedoston nimi:")
        vaalitiedosto = input("> ")

    vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_vaalitiedosto(vaalitiedosto)

    print(
        "Jättäytyykö joku ehdokas pois? Syötä 'y' jos joku jättäytyy, muuten paina enteriä:"
    )
    joku_jättäytyy = input("> ")
    print()

    if joku_jättäytyy == "y":
        jättäytyneet = kysy_jättäytyneet(ehdokkaat)
        poista_jättäytyneet_lipukkeista(jättäytyneet, lipukkeet)
        ehdokkaat = [
            ehdokas for ehdokas in ehdokkaat if ehdokas.tila != Tila.Jättäytynyt
        ]

    print(f"Vaali: {vaalin_nimi}\n\n")

    suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet)

    lokihakemisto = "vaalit"
    luo_lokihakemisto(lokihakemisto)

    print()
    vaalin_nimi = vaalin_nimi.replace(" ", "_")
    aikaleima = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    loki_tiedosto = f"{vaalin_nimi}_{aikaleima}.log"
    with open(f"{lokihakemisto}/{loki_tiedosto}", "x") as f:
        print(f"Kirjoitetaan logit tiedostoon '{os.path.abspath(f.name)}'")
        vaalilogger.tulosta_tiedostoon(f)


if __name__ == "__main__":
    try:
        main()
    except VaaliException as e:
        print("Virhe:", e)
