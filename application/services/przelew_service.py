from __future__ import annotations
from dataclasses import dataclass
from ..models_.konto_model import Transakcja
from application.services.service_base import ServiceBase

class PrzelewService(ServiceBase):

    @dataclass
    class Request:
        transakcja: Transakcja

    @dataclass
    class Response:
        status: bool
        #Ewentualnie do zmiany gdybysmy chcieli czegos wiecej niz ok/nie ok

    def wykonaj_przelew(self, request: PrzelewService.Request) -> PrzelewService.Response:
        self.validate_request(request)
        #TODO
        return PrzelewService.Response(status=True)



