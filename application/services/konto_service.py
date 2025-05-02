from __future__ import annotations
from ..models_.konto_model import KontoUzytkownika
import uuid
from dataclasses import dataclass
from application.services.service_base import ServiceBase

class KontoUzytkownikaService(ServiceBase):

    @dataclass
    class Request:
        id_konta: uuid.UUID

    @dataclass
    class Response:
        konto_uzytkownika: KontoUzytkownika
        status: bool

    def daj_konto(self, request: KontoUzytkownikaService.Request) -> KontoUzytkownikaService.Response:
        self.validate_request(request=request)
        #TODO
        pass


    def czy_istnieje(self, request: KontoUzytkownikaService.Request) -> bool:
        self.validate_request(request=request)
        #TODO
        pass

        #TODO
        #1. Polaczenie z baza
        #2. Query na konto po id
        #3. Zwroc konto albo nulla???
        pass