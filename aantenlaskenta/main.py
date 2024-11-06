import opavote

if __name__ == "__main__":

    with open("testivaali.txt") as f:
        vaalin_nimi, paikkamäärä, ehdokkaat, lipukkeet = opavote.lue_lipukkeet(f.readlines())

    print(vaalin_nimi)

    print()
    print("Ehdokkaat:")

    for ehdokas in ehdokkaat:
        print(ehdokas)

