from dataclasses import dataclass
from application.models import Account, Transaction
from application.services.database import get_db_session


class TransferFunds:
    @dataclass
    class Request:
        transaction: Transaction

    @dataclass
    class Response:
        transaction_id: int

    @staticmethod
    async def handle(request) -> "TransferFunds.Response":
        if not isinstance(request, TransferFunds.Request):
            raise ValueError(
                f"Otrzymany request: {type(request).__name__} nie jest typu WyslijPrzelew.Request"
            )

        with get_db_session() as db_session:

            source_account = (
                db_session.query(Account)
                .filter(Account.id == request.transaction.source_account_id)
                .first()
            )
            target_account = (
                db_session.query(Account)
                .filter(Account.id == request.transaction.target_account_id)
                .first()
            )

            TransferFunds.validate(
                source_account, target_account, request.transaction.amount_numeric
            )

            try:
                transakcja = Transaction(
                    amount_numeric=request.transaction.amount_numeric,
                    source_account_id=request.transaction.source_account_id,
                    target_account_id=request.transaction.target_account_id,
                    description=request.transaction.description,
                )

                db_session.add(transakcja)

                source_account.balance -= request.transaction.amount_numeric
                target_account.balance += request.transaction.amount_numeric

                db_session.commit()
                return TransferFunds.Response(transaction_id=transakcja.id)
            except Exception as exc:
                print(exc, flush=True)
                raise RuntimeError(
                    "Transakcja nie doszła do skutku, coś poszło nie tak."
                )

    @staticmethod
    def validate(
        source_account: Account, target_account: Account, amount: float
    ) -> None:
        if source_account is None:
            raise ValueError("Nie znaleziono nadawcy.")
        if target_account is None:
            raise ValueError("Nie znaleziono adresata.")
        if source_account.currency != target_account.currency:
            raise ValueError("Konta adresata i nadawcy są w różnych walutach.")
        if source_account.id == target_account.id:
            raise ValueError("Numer konta adresata i nadawcy nie może być taki sam.")
        if source_account.balance - amount < 0:
            raise ValueError("Niewystarczające środki na koncie.")
