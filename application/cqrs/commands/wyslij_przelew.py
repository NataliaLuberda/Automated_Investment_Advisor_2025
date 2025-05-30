from application.models import Account, Transakcja, Currency
from application.utils.waluty import Waluta
from application.services.database import get_db_session
from sqlalchemy import exists
import sys

class WyslijPrzelew:
    
    class Request:
        def __init__(self) -> None:
            self.id_nadawcy: int
            self.id_adresata: int
            self.kwota: float
            self.waluta: 'Waluta'
    
    class Response:
        def __init__(self, id_transakcji) -> None:
            self.id_transakcji: int = id_transakcji
        
    def handle(self, request: WyslijPrzelew.Request) -> 'WyslijPrzelew.Response':
        if (type(WyslijPrzelew.Request) != type(request)):
            raise ValueError("Typ Requesta != WyslijPrzelew.Request")
        
        db_session = get_db_session()
        
        waluta_id = db_session.query(Currency).filter(Currency.name == request.waluta.name).first()
        konto_nadawcy_istnieje = db_session.query(exists().where(Account.id == request.id_nadawcy)).scalar()
        konto_adresata_istnieje = db_session.query(exists().where(Account.id == request.id_adresata)).scalar()
        
        if konto_adresata_istnieje is False or konto_nadawcy_istnieje is False:
            raise ValueError("Błędne id konta adresata lub nadawcy.")
        
        if waluta_id is None:
            raise ValueError("Nie znaleziono waluty podanej w WyslijPrzelew.Request")
        
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
        
        