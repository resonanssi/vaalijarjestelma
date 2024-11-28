import vaali

def test_ylöspyöristys():
    arvot = [
        (1.1234567, 1.12346),
        (1.0000112, 1.00002),
        (1.0000000, 1.00000),
        (1.1291013, 1.12911),
        (3.1415926, 3.14160)
    ]

    for (testiarvo, oikea) in arvot:
        assert vaali.ceil_5dec(testiarvo) == oikea
