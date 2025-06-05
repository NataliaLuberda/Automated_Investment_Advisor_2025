from application.models import Account, Transakcja, Currency
from application.services.database import get_db_session
from dataclasses import dataclass

class WyslijPrzelew:
    
    @dataclass
    class Request:
        id_nadawcy: int
        id_adresata: int
        kwota: float
        opis: str

    @dataclass
    class Response:
        id_transakcji: int

    @staticmethod
    async def handle(request) -> 'WyslijPrzelew.Response':
        if not isinstance(request, WyslijPrzelew.Request):
            raise ValueError(f"Otrzymany request: {type(request).__name__} nie jest typu WyslijPrzelew.Request")

        db_session = get_db_session()

        konto_nadawcy = db_session.query(Account).filter(Account.id == request.id_nadawcy).first()
        konto_adresata = db_session.query(Account).filter(Account.id == request.id_adresata).first()

        WyslijPrzelew.validate(konto_nadawcy, konto_adresata, request.kwota)

        try:
            transakcja = Transakcja(
                amount_numeric=request.kwota,
                id_sender=request.id_nadawcy,
                id_receiver=request.id_adresata,
                description=request.opis
            )

            db_session.add(transakcja)

            konto_nadawcy.balance -= request.kwota
            konto_adresata.balance += request.kwota

            db_session.commit()
            return WyslijPrzelew.Response(id_transakcji=transakcja.id)
        except Exception as exc:
            print(exc, flush=True)
            raise RuntimeError("Transakcja nie doszła do skutku, coś poszło nie tak.")

    @staticmethod
    def validate(nadawca: Account, adresat: Account, kwota: float) -> None:
        if nadawca is None:
            raise ValueError("Nie znaleziono nadawcy.")
        if adresat is None:
            raise ValueError("Nie znaleziono adresata.")
        if nadawca.currency != adresat.currency:
            raise ValueError("Konta adresata i nadawcy są w różnych walutach.")
        if nadawca.balance - kwota < 0:
            raise ValueError("Niewystarczające środki na koncie.")
