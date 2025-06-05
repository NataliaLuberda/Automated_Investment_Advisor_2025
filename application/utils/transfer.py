from application.models import User, Account
from application.services.database import SessionLocal
from application.session import get_logged_user_email
from application.utils.currency import convert_between_currencies


def transfer_between_accounts(from_account_id: int, to_currency: str, amount: float) -> str:
    db = SessionLocal()
    try:
        email = get_logged_user_email()
        if not email:
            return "❌ Użytkownik niezalogowany!"
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return "❌ Użytkownik nie istnieje!"

        from_acc = db.query(Account).filter_by(id=from_account_id, user_id=user.id).first()
        to_acc = db.query(Account).filter_by(currency=to_currency.upper(), user_id=user.id).first()

        if not from_acc:
            return "❌ Konto źródłowe nie istnieje!"
        if amount <= 0:
            return "⚠️ Kwota musi być większa od zera!"
        if from_acc.balance < amount:
            return "❌ Za mało środków!"

        if not to_acc:
            to_acc = Account(currency=to_currency.upper(), balance=0.0, user_id=user.id)
            db.add(to_acc)
            db.commit()
            db.refresh(to_acc)

        if from_acc.currency == to_acc.currency and from_acc.id == to_acc.id:
            return "⚠️ Nie można przelać na to samo konto!"

        try:
            converted_amount = convert_between_currencies(amount, from_acc.currency, to_acc.currency)
        except Exception as e:
            return f"❌ Błąd konwersji: {e}"

        from_acc.balance -= amount
        to_acc.balance += converted_amount

        db.commit()
        return (f"✅ Przelano {amount:.2f} {from_acc.currency} "
                f"(~{converted_amount:.2f} {to_acc.currency})")
    finally:
        db.close()
