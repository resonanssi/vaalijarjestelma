## TKO-äly ry:n ääntenlaskuohjelma

Linkki ääni- ja vaalijärjestykseen: https://www.tko-aly.fi/yhdistys/vaalijarjestys

## Ohjelman suoritus

Varmista, että koneellasi on tarpeeksi uusi versio Pythonista (vähintään 3.10).

Asenna ohjelma koneellesi esimerkiksi 

- kloonaamalla gitillä
- lataamalla Zip-tiedoston Githubista ja purkamalla tiedoston

Avaa komentorivi ja siirry projektin juureen.

Suorita ohjelma komennolla:

```
  python main.py [vaalitiedosto]
```

Ohjelma tulostaa näytölle vaalin kulun, 
ja lisätietoja vaalit-nimiseen kansioon omaan tiedostoonsa.

## Muokkaaminen

Ohjelman kehittämisessä on helpointa käyttää Poetry-työkalua.

Aluksi aja ohjelman hakemistossa komento `poetry install` 
asentaaksesi vaadittavat riippuvuudet, kuten pytestin.

### Testaaminen

```
  [poetry run] pytest
```

### Koodin jäsentäminen

```
  [poetry run] ruff format
```

### Tyypityksen tarkistaminen

Varsinaiselle ohjelmalle:

```
  [poetry run] mypy aantenlaskenta/
```

Testeille:

```
  [poetry run] mypy tests/
```

Kaikkien komentojen pitäisi toimia ilman Poetryäkin, 
kunhan tarvittavat työkalut on asennettu jotain muuta kautta.

## Opavote

Äänestykseen käytetään Opavote-palvelua, 
josta äänestyksen loputtua saa ladattua äänet ja ehdokkaan sisältävän tiedoston. Tiedosto voi näyttää esimerkiksi tältä:

```
4 2
1 1 2 3 4 0
1 2 1 3 4 0
1 1 2 3 4 0
1 2 1 3 4 0
0
"Anna A."
"Bruno B."
"Charlie C."
"Daniela D."
"Joku vaali"
```

Tiedoston tulkitseminen tapahtuu näin:

Ensimmäisellä rivillä on kaksi lukua, ehdokkaiden lukumäärä ja valittavien henkilöiden määrä. 
Esimerkissä ehdokkaita on siis 4, ja paikkoja 2.

Sitä seuraa itse äänet. Jokainen äänirivi alkaa ykkösellä ja loppuu nollaan, ja niiden välillä sijaitsevat
itse äänet. Esimerkiksi ensimmäinen ääni `1 1 2 3 4 0` tarkoittaa siis, että äänestäjä on antanut äänensä järjestyksessä
1, 2, 3, 4, missä numerot viittaavat ehdokkaisiin siinä järjestyksessä, missä ne on tiedoston lopussa ilmoitettu.

Ääniä luetaan niin kauan, kunnes tulee pelkän yhden nollan sisältävä rivi. 

Tämän jälkeen seuraa ehdokkaiden nimet. Esimerkissä "Anna A." on numero 1, "Bruno B." numero 2, jne. 
Kun ehdokkaita on luettu ensimmäisellä rivillä määritellyn määrän verran, ollaan luettu kaikki ehdokkaat.

Viimeisellä rivillä on vielä vaalin nimi. Esimerkissä "Joku vaali"

```
[ehdokkaiden määrä] [paikkojen määrä]
1 [äänet] 0
1 [äänet] 0
1 [äänet] 0
...
0
"[ehdokas 1]"
"[ehdokas 2]"
"[ehdokas 3]"
...
"[vaalin nimi]"
```
