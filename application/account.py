from application.models import Account, User
from application.services.database import SessionLocal
from application.services.database import get_db_session
from application.session import get_logged_user_email
from application.utils.catched_total_balance import reset_user_balance


def get_user_accounts() -> list[Account]:
    with get_db_session() as db:
        email = get_logged_user_email()
        user = db.query(User).filter_by(email=email).first()
        accounts = user.accounts if user else []
        return accounts


def set_account_balance(user, currency: str, new_balance: float):
    with get_db_session() as db:
        acc = db.query(Account).filter_by(currency=currency, user_id=user.id).first()
        if not acc:
            return False
        acc.balance = new_balance
        db.commit()
        reset_user_balance(user.email)
        return True


def create_account(currency: str, balance: float) -> str:
    with get_db_session() as db:
        db = SessionLocal()
        email = get_logged_user_email()
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return "❌ Użytkownik niezalogowany"

        existing = db.query(Account).filter_by(currency=currency.strip().upper(), user_id=user.id).first()

        if existing:
            return "⚠️ Konto w tej walucie już istnieje"

        add_account_for_user(user, currency, balance)
        return f"✅ Dodano konto: {currency.upper()} ({balance:.2f})"


def add_account_for_user(user, currency: str, start_balance: float = 0.0):
    with get_db_session() as db:
        currency = currency.strip().upper()
        existing = db.query(Account).filter_by(currency=currency, user_id=user.id).first()
        if existing:
            return existing
        acc = Account(currency=currency, balance=start_balance, user_id=user.id)
        db.add(acc)
        db.commit()
        db.refresh(acc)
        reset_user_balance(user.email)
        return acc


def delete_account(account_id: int):
    with get_db_session() as db:
        email = get_logged_user_email()
        user = db.query(User).filter_by(email=email).first()

        if not user:
            raise Exception("❌ Użytkownik niezalogowany!")

        account = db.query(Account).filter_by(id=account_id, user_id=user.id).first()
        if not account:
            raise Exception("❌ Konto w danej walucie nie istnieje!")

        if account.balance > 0:
            raise Exception("❌ Konto zawiera środki! Przenieś je, a następnie usuń konto.")

        db.delete(account)
        db.commit()
        return f"✅ Usunięto konto: {account.currency}"


def update_account_balance(account_id: int, new_balance: float) -> str:
    with get_db_session() as db:
        email = get_logged_user_email()
        user = db.query(User).filter_by(email=email).first()

        if not user:
            return "❌ Operacja nie powiodła się!"

        account = db.query(Account).filter_by(id=account_id, user_id=user.id).first()

        if not account:
            return "❌ Operacja nie powiodła się!"

        account.balance = new_balance
        db.commit()
        return f"✏️ Zaktualizowano saldo konta {account.currency} na {new_balance:.2f}"


def update_default_account_currency(selected_code: str):
    with get_db_session() as db:
        email = get_logged_user_email()
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return "❌ Operacja nie powiodła się!"

        existing = db.query(Account).filter_by(currency=selected_code.strip().upper(), user_id=user.id).first()
        if not existing:
            acc = Account(currency=selected_code.strip().upper(), balance=0.0, user_id=user.id)
            db.add(acc)
            db.commit()
            db.refresh(acc)

        user.default_currency = selected_code.strip().upper()
        db.commit()
        return f"✏️ Zaktualizowano konto domyślne na {selected_code.upper()} (jeśli nie miałeś konta, już je masz 😎)"
