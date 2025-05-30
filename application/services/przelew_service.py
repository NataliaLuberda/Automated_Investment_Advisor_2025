from __future__ import annotations
from dataclasses import dataclass
from ..models_.transakcja_model import Transakcja
from ..services.base_service import BaseService
from time import sleep

class PrzelewService(BaseService):

    @dataclass
    class Request:
        transakcja: Transakcja

    @dataclass
    class Response:
        status_ok: bool
        #Ewentualnie do zmiany gdybysmy chcieli czegos wiecej niz ok/nie ok

    def validate_request(self, request: PrzelewService.Request) -> None:
        return
    
    async def handle(self, request: PrzelewService.Request) -> PrzelewService.Response:

        #TODO wyslanie przelewu do bazy itp itd
        
        
        
        sleep(1)
        
        return PrzelewService.Response(status_ok=True)