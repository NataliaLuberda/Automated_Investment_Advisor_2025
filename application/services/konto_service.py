from __future__ import annotations
from ..models_.konto_uzytkownika_model import KontoUzytkownika
import uuid
from dataclasses import dataclass
from ..services.base_service import BaseService
from ..models_.rachunek_bankowy_model import RachunekBankowy

class KontoUzytkownikaService(BaseService):

    @dataclass
    class Request:
        id_konta: uuid.UUID

    @dataclass
    class Response:
        konto_uzytkownika: KontoUzytkownika
        status: bool

    def daj_konto(self, request: KontoUzytkownikaService.Request) -> KontoUzytkownikaService.Response:
        self.validate_request(request=request)

                
        
        return KontoUzytkownikaService.Response(KontoUzytkownika('a', 'b'), True)