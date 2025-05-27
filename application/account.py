import requests

from application.database import SessionLocal
from application.models import Account, User
from application.session import get_logged_user_email

API_KEY = "cur_live_WllS2ns9qh9K1PIRxkpLkFoYgYc6shSXDvZBnO51"


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


def convert_between_currencies(amount: float, from_currency: str, to_currency: str) -> float:
    try:
        if from_currency == to_currency:
            return round(amount, 2)

        rates = get_currencyapi_rates(base_currency=from_currency, symbols=[to_currency])
        converted = amount * rates[to_currency]
        return round(converted, 2)

    except KeyError:
        raise ValueError(f"Brak kursu waluty: {from_currency} → {to_currency}")
    except Exception as e:
        raise ValueError(f"Błąd konwersji {from_currency} → {to_currency}: {e}")


def get_currencyapi_rates(base_currency: str = "PLN", symbols: list[str] = None) -> dict:
    if symbols is None:
        symbols = ["USD", "EUR", "GBP", "CAD"]

    symbols_param = ",".join(symbols)
    url = f"https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={base_currency}&currencies={symbols_param}"

    try:
        response = requests.get(url)
        data = response.json()

        if "data" not in data:
            raise ValueError(f"Nie udało się pobrać kursów: {data}")

        rates = {}
        for symbol in symbols:
            try:
                rates[symbol] = data["data"][symbol]["value"]
            except KeyError:
                raise ValueError(f"❌ Brak kursu {symbol} względem {base_currency}")
        return rates

    except Exception as e:
        raise ValueError(f"❌ {e}")
