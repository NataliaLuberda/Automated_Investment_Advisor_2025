from __future__ import annotations

import uuid

from application.utils.waluty import Waluta
from .rachunek_bankowy_model import RachunekBankowy


class KontoUzytkownika:
    def __init__(self, imie: str, nazwisko: str) -> None:
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
