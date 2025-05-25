from application.database import SessionLocal
from application.models import Account, User
from application.session import get_logged_user_email


def get_user_accounts():
    db = SessionLocal()
    email = get_logged_user_email()
    user = db.query(User).filter_by(email=email).first()
    accounts = user.accounts if user else []
    db.close()
    return accounts


def create_account(currency: str, balance: float) -> str:
    db = SessionLocal()
    email = get_logged_user_email()
    user = db.query(User).filter_by(email=email).first()
    currency = currency.strip().upper()

    if not user:
        return "❌ Użytkownik niezalogowany"

    if any(acc.currency == currency for acc in user.accounts):
        return "⚠️ Konto w tej walucie już istnieje"

    new_acc = Account(currency=currency, balance=balance, user_id=user.id)
    db.add(new_acc)
    db.commit()
    db.close()
    return f"✅ Dodano konto: {currency} ({balance:.2f})"
