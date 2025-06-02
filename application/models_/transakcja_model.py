from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from application.utils.waluty import Waluta


@dataclass(frozen=True)
class Transakcja:
    id_rachunku_zrodlowego: int
    id_rachunku_adresata: int
    kwota: float
    opis: str
    waluta: 'Waluta'


class TransakcjaBuilder:
    """Builder dla klasy Transakcja
    #### Pola:
        - od [nadawca]: uuid.UUID
        - do (adresat): uuid.UUID
        - kwota (> 0): float
        - timestamp: datetime
        - opis: str
    #### Metody:
    - def build(): zwraca instancję klasy Transakcja
    - def with_time_now(): ustawia datetime na datetime.now()
    - def with_datetime(datetime): ustawia self.datetime na datetime
    - def czy_poprawne_parametry()
    """

    DLUGOSC_OPISU_LIMIT: int = 128

    def __init__(self):

        self._od: Optional[uuid.UUID] = None
        self._do: Optional[uuid.UUID] = None
        self._kwota: Optional[float] = None
        self._opis: str = ""
        self._waluta: Waluta = Waluta.PLN

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
            raise ValueError("Kwota transkacji nie może byc <= 0!")
        self._kwota = value

    @property
    def opis(self) -> Optional[str]:
        return self._opis

    @opis.setter
    def opis(self, opis: str):
        self._opis = opis

    @property
    def waluta(self) -> 'Waluta':
        return self._waluta

    @waluta.setter
    def waluta(self, waluta: Waluta) -> None:
        self._waluta = waluta

    def build(self) -> Transakcja:
        return Transakcja(
            id_rachunku_zrodlowego=self._od,  # type: ignore
            id_rachunku_adresata=self._do,  # type: ignore
            kwota=self._kwota,  # type: ignore
            opis=self._opis,
            waluta=self._waluta
        )

    def czy_poprawne_parametry(self) -> bool:
        if not isinstance(self._od, int) or not isinstance(self._do, int):
            return False
        if not isinstance(self._kwota, float):
            return False
        if not isinstance(self._opis, str):
            return False
        if len(self._opis) > TransakcjaBuilder.DLUGOSC_OPISU_LIMIT:
            return False
        return True
