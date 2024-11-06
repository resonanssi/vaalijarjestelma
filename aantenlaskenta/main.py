import opavote
from ehdokas import Ehdokas, Tila
from lipuke import Lipuke
from vaali import suorita_vaali


def kysy_jättäytyneet(ehdokkaat: list[Ehdokas]):
    print("Kuka/ketkä ehdokkaista jättäytyvät?\n")

    for ehdokas in ehdokkaat:
        print(f"[{ehdokas._id}]: {ehdokas.nimi}")

    print("\nSyötä pois jättäytyvän ehdokkaan id (nimeä edeltävä numero).")
    print("Jos pois jättäytyviä ehdokkaita on monta, syötä ne kaikki pilkulla erotettuna.")
    print("Esimerkiksi: 2, 3, 10\n")

    syöte = input("> ").strip().split(",")    
    pois_jättäytyvät_id = [int(id) for id in syöte]
    pois_jättäytyvät = []

    for id in pois_jättäytyvät_id:
        filtteröidyt = list(filter(lambda ehdokas: ehdokas._id == id, ehdokkaat))

        if len(filtteröidyt) == 0:
            raise Exception(f"Ehdokasta numero {id} ei löytynyt! Keskeytetään")

        ehdokas = filtteröidyt[0]
        print(f"Merkitään ehdokas {ehdokas.nimi} jättäytyneeksi pois")
        pois_jättäytyvät.append(ehdokas)

    return pois_jättäytyvät
    

def poista_jättäytyneet_lipukkeista(jättäytyneet: list[Ehdokas], lipukkeet: list[Lipuke]):
    for ehdokas in jättäytyneet:
        ehdokas.tila = Tila.Jättäytynyt

    jättäytyneet_id = [ehdokas._id for ehdokas in jättäytyneet]

    for lipuke in lipukkeet:
        lipuke.ehdokkaat = [id for id in lipuke.ehdokkaat if id not in jättäytyneet_id]
    

if __name__ == "__main__":

    with open("testivaali.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = opavote.lue_lipukkeet(f.readlines())

    joku_jättäytyy = input("Jättäytyykö joku ehdokas pois? [y/N]: ")

    if joku_jättäytyy == "y":
        jättäytyneet = kysy_jättäytyneet(ehdokkaat)
        poista_jättäytyneet_lipukkeista(jättäytyneet, lipukkeet)

    print(vaalin_nimi)
    print()

    for ehdokas in ehdokkaat:
        print(f"Ehdokas {ehdokas.nimi}: {ehdokas.tila}")

    print()

    for lipuke in lipukkeet:
        print(lipuke.ehdokkaat)
    # suorita_vaali(paikkamäärä, ehdokkaat, lipukkeet)
