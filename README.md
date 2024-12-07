## TKO-äly ry:n ääntenlaskuohjelma

Linkki ääni- ja vaalijärjestykseen: https://www.tko-aly.fi/yhdistys/vaalijarjestys

## Ohjelman suoritus

Varmista, että koneellasi on tarpeeksi uusi versio Pythonista (vähintään 3.10).

Asenna ohjelma koneellesi esimerkiksi 

- kloonaamalla gitillä
- lataamalla Zip-tiedoston Githubista ja purkamalla tiedoston

Avaa komentorivi ja siirry ohjelmakansioon (`aantenlaskenta/`).

Suorita ohjelma komennolla:

```
  python aantenlaskenta/main.py [vaalitiedosto]
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
