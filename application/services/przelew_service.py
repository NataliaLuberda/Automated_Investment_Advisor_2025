from ..models_.konto_model import Transakcja

class PrzelewService:
    def __init__(self):
        pass
    
    class Request:
        def __init__(self, transakcja: Transakcja):
            self._transakcja = transakcja
    
    class Response:
        def __init__(self):
            self._czyOk: bool = False

    def handle() -> "PrzelewService.Response":
        pass



