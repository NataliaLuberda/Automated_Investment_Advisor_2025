from application.models import Account, Transakcja, Currency
from application.utils.waluty import Waluta
from application.services.database import get_db_session
from sqlalchemy import exists
import sys

class WyslijPrzelew:
    
    class Request:
        def __init__(self, id_nadawcy: int, id_adresata: int, kwota: float, waluta: 'Waluta', opis: str) -> None:
            self.id_nadawcy: int = id_nadawcy
            self.id_adresata: int = id_adresata
            self.kwota: float = kwota
            self.waluta: 'Waluta' = waluta
            self.opis: str = opis
    
    class Response:
        def __init__(self, id_transakcji) -> None:
            self.id_transakcji: int = id_transakcji
        
    async def handle(self, request) -> 'WyslijPrzelew.Response':
        if not isinstance(request, WyslijPrzelew.Request):
            raise ValueError(f"Otrzymany request: {type(request).__name__} nie jest typu WyslijPrzelew.Request")
        
        db_session = get_db_session()
        
        waluta = db_session.query(Currency).filter(Currency.name == request.waluta.name).first()
        
        konto_nadawcy = db_session.query(Account).filter(Account.id == request.id_nadawcy).first()
        konto_adresata = db_session.query(Account).filter(Account.id == request.id_adresata).first()
        
        self.validate(konto_nadawcy, konto_adresata, waluta, request.kwota)
        
        try:
            transakcja = Transakcja(
                amount_numeric = request.kwota,
                id_sender = request.id_nadawcy,
                id_receiver = request.id_adresata,
                currency_id = waluta.id,
                description=request.opis
                )
            
            db_session.add(transakcja)
            
            konto_nadawcy.balance -= request.kwota
            konto_adresata.balance += request.kwota
            
            db_session.commit()
            return WyslijPrzelew.Response(id_transakcji = transakcja.id)
        except Exception as exc:
            raise RuntimeError("Transakcja nie doszła do skutku, coś poszło nie tak.")
            
        
    def validate(self, nadawca: Account, adresat: Account, waluta: Waluta, kwota: float) -> None:
        
        if waluta is None:
            raise ValueError("Nie znaleziono waluty podanej w WyslijPrzelew.Request.")
        if nadawca is None:
            raise ValueError("Nie znaleziono nadawcy.")
        if adresat is None:
            raise ValueError("Nie znaleziono adresata.")
        if nadawca.currency != adresat.currency:
            raise ValueError("Konta adresata i nadawcy są w różnych walutach.")
        if nadawca.balance - kwota < 0:
            raise ValueError("Niewystarczające środki na koncie.")
