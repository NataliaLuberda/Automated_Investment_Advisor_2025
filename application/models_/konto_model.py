import uuid
from utility.waluty import Waluta

class KontoUzytkownika:
    def __init__(self, imie: str, nazwisko: str, stan_konta: float) -> 'KontoUzytkownika':
        self._id = uuid.uuid4()
        self._imie = imie
        self._nazwisko = nazwisko
        self._stan_konta = stan_konta
        self._rachunki_bankowe: list[RachunekBankowy]

    def daj_id(self) -> uuid.UUID:
        return self._id
    
    def daj_imie_nazwisko(self) -> str:
        return f"{self._imie} {self._nazwisko}"
    
    def dodaj_rachunek_bankowy(self, waluta: Waluta, kwota: float = 0, ) -> None:
        self._rachunki_bankowe.append(RachunekBankowy(kwota=kwota, rodzaj_waluty=waluta))

class RachunekBankowy:
    def __init__(self, kwota: float, rodzaj_waluty: Waluta):
        self._id = uuid.uuid4()
        self._kwota: float = kwota
        self._waluta: Waluta = rodzaj_waluty

    def get_kwota(self) -> float:
        return self._kwota
