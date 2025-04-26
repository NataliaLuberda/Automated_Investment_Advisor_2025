import uuid
from ..utility.waluty import Waluta
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

class ModelStronyKonto:
    pass

class KontoUzytkownika:
    def __init__(self, imie: str, nazwisko: str) -> 'KontoUzytkownika':
        self._id = uuid.uuid4()
        self._imie = imie
        self._nazwisko = nazwisko
        self._rachunki_bankowe: list[RachunekBankowy] = list()

    def daj_id(self) -> uuid.UUID:
        return self._id
    
    @property
    def imie(self):
        return self._imie

    def daj_imie_nazwisko(self) -> str:
        return f"{self._imie} {self._nazwisko}"
    
    def dodaj_rachunek_bankowy(self, waluta: Waluta, kwota: float = 0, ) -> None:
        self._rachunki_bankowe.append(RachunekBankowy(self._id, kwota=kwota, rodzaj_waluty=waluta))

    def daj_rachunki_uzytkownika(self) -> list['RachunekBankowy']:
        return self._rachunki_bankowe

class RachunekBankowy:
    def __init__(self, id_wlasciciela: uuid.UUID, kwota: float, rodzaj_waluty: Waluta):
        self._id_wlasciciela = id_wlasciciela
        self._id = uuid.uuid4()
        self._kwota: float = kwota
        self._waluta: Waluta = rodzaj_waluty
        self._transakcje: list[Transakcja] = list()
    
    @property
    def kwota(self) -> float:
        return self._kwota
    
    @property
    def id_wlasciciela(self) -> uuid.UUID:
        return self._id_wlasciciela

    @property
    def id(self) -> uuid.UUID:
        return self._id

# class Transakcja:
#     def __init__(self, od: uuid.UUID, do: uuid.UUID, timestamp: datetime, kwota: float):
#         self._id_rachunku_zrodlowego: uuid.UUID = od
#         self._id_rachunku_adresata: uuid.UUID = do
#         self._timestamp: datetime = timestamp
#         self._kwota: float = kwota
    
#     @property
#     def id_rachunku_zrodlowego(self) -> uuid.UUID:
#         return self._id_rachunku_zrodlowego
    
#     @property
#     def id_rachunku_adresata(self) -> uuid.UUID:
#         return self._id_rachunku_adresata
    
#     @property
#     def timestamp(self) -> datetime:
#         return self._timestamp
    
#     @property
#     def kwota(self) -> float:
#         return self._kwota

@dataclass(frozen=True)
class Transakcja:
    id_rachunku_zrodlowego: uuid.UUID
    id_rachunku_adresata: uuid.UUID
    timestamp: datetime
    kwota: float

class TransakcjaBuilder:
    def __init__(self):
        self._od = None
        self._do = None
        self._kwota = None
        self._timestamp = None
    
    @property
    def od(self) -> Optional[uuid.UUID]:
        return self._od

    @od.setter
    def od(self, value: uuid.UUID):
        self._od = value

    @property
    def do(self) -> Optional[uuid.UUID]:
        return self._do

    @do.setter
    def do(self, value: uuid.UUID):
        self._do = value

    @property
    def kwota(self) -> Optional[float]:
        return self._kwota

    @kwota.setter
    def kwota(self, value: float):
        if value <= 0:
            raise ValueError("Kwota must be positive")
        self._kwota = value

    @property
    def timestamp(self) -> Optional[datetime]:
        return self._timestamp or datetime.now()

    @timestamp.setter
    def timestamp(self, value: datetime):
        self._timestamp = value
    
    def build(self) -> Transakcja:
        if not self.czy_poprawne_parametry():
            raise ValueError("Transakcja ma błędne parametry")
        else:
            return Transakcja(
                id_rachunku_zrodlowego=self._od,
                id_rachunku_adresata=self._do,
                kwota=self._kwota,
                timestamp=self._timestamp
            )
    
    def czy_poprawne_parametry(self) -> bool:
        if None in (self._od, self._do, self._kwota, self._timestamp):
            return False
        else:
            return True