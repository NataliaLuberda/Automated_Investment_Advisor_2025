from sqlalchemy import or_

from application.models import Transaction
from application.services.database import get_db_session


def get_accounts_transaction_history(account_id: int) -> list[Transaction]:
    with get_db_session() as session:
        transactions = (
            session.query(Transaction)
            .filter(
                or_(
                    Transaction.target_account_id == account_id,
                    Transaction.source_account_id == account_id,
                )
            )
            .all()
        )

    return transactions
