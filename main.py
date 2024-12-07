from aantenlaskenta.main import aloita
from aantenlaskenta.utils import VaaliException

if __name__ == "__main__":
    try:
        aloita()
    except VaaliException as e:
        print("Virhe:", e)
