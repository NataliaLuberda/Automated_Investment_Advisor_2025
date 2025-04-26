import uuid

class Konto:
    def __init__(self, imie: str, nazwisko: str) -> 'Konto':
        self._id = uuid.uuid4()
        self._imie = imie
        self._nazwisko = nazwisko

    def daj_id(self) -> uuid.UUID:
        return self._id
    
    def daj_imie_nazwisko(self) -> str:
        return f"{self._imie} {self._nazwisko}"