from opavote import lue_lipukkeet
from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
from vaali import suorita_vaali
from vaalilogger import vaalilogger
from datetime import datetime
from utils import luo_lokihakemisto
import os


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
        raise Exception("Kirjoita syöte oikeassa muodossa!")

    pois_jättäytyvät = []

    for id in pois_jättäytyvät_id:
        filtteröidyt = list(filter(lambda ehdokas: ehdokas._id == id, ehdokkaat))

        if len(filtteröidyt) == 0:
            raise Exception(f"Ehdokasta numero {id} ei löytynyt!")

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


def main():
    print("Syötä vaalitiedoston nimi:")
    vaalitiedosto = input("> ")
    # vaalitiedosto = "pikkuvaali.txt"

    with open(vaalitiedosto) as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = lue_lipukkeet(f.readlines())

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
    aikaleima = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    loki_tiedosto = f"vaali_{aikaleima}.log"
    with open(f"{lokihakemisto}/{loki_tiedosto}", "x") as f:
        print(f"Kirjoitetaan logit tiedostoon '{os.path.abspath(loki_tiedosto)}'")
        vaalilogger.tulosta_tiedostoon(f)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Virhe:", e)
