from ..models_.transakcja_model import Transakcja
from ..utility.waluty import Waluta
import uuid

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