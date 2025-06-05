from application.models import Account, User
from application.services.database import SessionLocal
from application.session import get_logged_user_email
from application.utils.catched_total_balance import reset_user_balance


def get_user_accounts() -> list[Account]:
    db = SessionLocal()
    email = get_logged_user_email()
    user = db.query(User).filter_by(email=email).first()
    accounts = user.accounts if user else []
    db.close()
    return accounts


def set_account_balance(user, currency: str, new_balance: float):
    db = SessionLocal()
    acc = db.query(Account).filter_by(currency=currency, user_id=user.id).first()
    if not acc:
        db.close()
        return False
    acc.balance = new_balance
    db.commit()
    db.close()
    reset_user_balance(user.email)
    return True


def create_account(currency: str, balance: float) -> str:
    db = SessionLocal()
    email = get_logged_user_email()
    user = db.query(User).filter_by(email=email).first()
    if not user:
        db.close()
        return "❌ Użytkownik niezalogowany"
    existing = db.query(Account).filter_by(currency=currency.strip().upper(), user_id=user.id).first()
    if existing:
        db.close()
        return "⚠️ Konto w tej walucie już istnieje"
    db.close()
    add_account_for_user(user, currency, balance)
    return f"✅ Dodano konto: {currency.upper()} ({balance:.2f})"


def add_account_for_user(user, currency: str, start_balance: float = 0.0):
    db = SessionLocal()
    currency = currency.strip().upper()
    existing = db.query(Account).filter_by(currency=currency, user_id=user.id).first()
    if existing:
        db.close()
        return existing
    acc = Account(currency=currency, balance=start_balance, user_id=user.id)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    db.close()
    reset_user_balance(user.email)
    return acc


def delete_account(account_id: int):
    db = SessionLocal()
    email = get_logged_user_email()
    user = db.query(User).filter_by(email=email).first()

    if not user:
        db.close()
        raise Exception("❌ Użytkownik niezalogowany!")

    account = db.query(Account).filter_by(id=account_id, user_id=user.id).first()
    if not account:
        db.close()
        raise Exception("❌ Konto w danej walucie nie istnieje!")

    if account.balance > 0:
        db.close()
        raise Exception("❌ Konto zawiera środki! Przenieś je, a następnie usuń konto.")

    db.delete(account)
    db.commit()
    db.close()
    return f"✅ Usunięto konto: {account.currency}"


def update_account_balance(account_id: int, new_balance: float) -> str:
    db = SessionLocal()
    email = get_logged_user_email()
    user = db.query(User).filter_by(email=email).first()

    if not user:
        db.close()
        return "❌ Operacja nie powiodła się!"

    account = db.query(Account).filter_by(id=account_id, user_id=user.id).first()

    if not account:
        db.close()
        return "❌ Operacja nie powiodła się!"

    account.balance = new_balance
    db.commit()
    db.close()
    return f"✏️ Zaktualizowano saldo konta {account.currency} na {new_balance:.2f}"
