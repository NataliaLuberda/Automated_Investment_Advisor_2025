from __future__ import annotations
from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Transakcja:
    id_rachunku_zrodlowego: uuid.UUID
    id_rachunku_adresata: uuid.UUID
    timestamp: datetime
    kwota: float
    opis: str

class TransakcjaBuilder:
    
    DLUGOSC_OPISU_LIMIT: int = 256
    
    def __init__(self):
        self._od: Optional[uuid.UUID] = None
        self._do: Optional[uuid.UUID] = None
        self._kwota: Optional[float] = None
        self._timestamp: Optional[datetime] = None
        self._opis: str = ""
    
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
    def timestamp(self) -> Optional[datetime]:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime):
        self._timestamp = value
        
    def with_timestamp(self, timestamp: datetime) -> TransakcjaBuilder:
        self._timestamp = timestamp
        return self
    
    def with_time_now(self) -> TransakcjaBuilder:
        self._timestamp = datetime.now()
        return self
    
    @property
    def opis(self) -> Optional[str]:
        return self._opis
    
    @opis.setter
    def opis(self, opis: str):
        self._opis = opis
    
    def build(self) -> Transakcja:
        # if not self.czy_poprawne_parametry():
        #     raise ValueError("Transakcja ma błędne parametry")
        # else:
        #     return Transakcja(
        #         id_rachunku_zrodlowego=self._od,
        #         id_rachunku_adresata=self._do,
        #         kwota=self._kwota,
        #         timestamp=self._timestamp,
        #         opis=self._opis
        #     )
        return Transakcja(
                id_rachunku_zrodlowego=self._od,
                id_rachunku_adresata=self._do,
                kwota=self._kwota,
                timestamp=self._timestamp,
                opis=self._opis
            )
    
    def czy_poprawne_parametry(self) -> bool:
        if not isinstance(self._od, uuid.UUID) or not isinstance(self._do, uuid.UUID):
            return False
        if not isinstance(self._kwota, float):
            return False
        if not isinstance(self._timestamp, datetime):
            return False
        if not isinstance(self._opis, str):
            return False
        if len(self._opis) > TransakcjaBuilder.DLUGOSC_OPISU_LIMIT:
            return False
        return True