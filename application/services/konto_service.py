from ..models_.konto_model import KontoUzytkownika
import uuid

class KontoUzytkownikaService:
    def __init__(self):
        pass

    class Request:
        def __init__(self, konto_uzytkownika_id: KontoUzytkownika):
            self._id: uuid.UUID = konto_uzytkownika_id

    class Response:
        def __init__(self):
            self._konto_uzytkownika: KontoUzytkownika
            self._czy_ok: bool

    def _handle():
        #TODO
        #1. Polaczenie z baza
        #2. Query na konto po id
        #3. Zwroc konto albo nulla???
        pass