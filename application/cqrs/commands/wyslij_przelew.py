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
        
        waluta_id = db_session.query(Currency).filter(Currency.name == request.waluta.name).first()
        konto_nadawcy_istnieje = db_session.query(exists().where(Account.id == request.id_nadawcy)).scalar()
        konto_adresata_istnieje = db_session.query(exists().where(Account.id == request.id_adresata)).scalar()
        
        if konto_adresata_istnieje is False or konto_nadawcy_istnieje is False:
            raise ValueError("Błędne id konta adresata lub nadawcy.")
        
        if waluta_id is None:
            raise ValueError("Nie znaleziono waluty podanej w WyslijPrzelew.Request")
        
        if len(request.opis) > 128:
            raise ValueError("Zbyt długi opis transakcji.")
        
        transakcja = Transakcja(
            amount_numeric = request.kwota,
            id_sender = request.id_nadawcy,
            id_receiver = request.id_adresata,
            currency = request.waluta,
            currency_id = waluta_id
            )
        
        db_session.add(transakcja)
        db_session.commit()
        
        return WyslijPrzelew.Response(id_transakcji = transakcja.id)
        
        