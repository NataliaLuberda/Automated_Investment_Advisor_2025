import uuid
import utility.waluty

class KontoUzytkownika:
    def __init__(self, imie: str, nazwisko: str, stan_konta: float) -> 'KontoUzytkownika':
        self._id = uuid.uuid4()
        self._imie = imie
        self._nazwisko = nazwisko
        self._stan_konta = stan_konta

    def daj_id(self) -> uuid.UUID:
        return self._id
    
    def daj_imie_nazwisko(self) -> str:
        return f"{self._imie} {self._nazwisko}"

class RachunekBankowy:
    def __init__(self, kwota: float, rodzaj_waluty: utility.waluty.Waluty):
        self._kwota: float = kwota
        self._waluta: utility.waluty.Waluty = rodzaj_waluty
