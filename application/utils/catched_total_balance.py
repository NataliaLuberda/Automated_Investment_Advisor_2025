from application.auth import get_user_by_email
from application.utils.currency import convert_between_currencies

_user_balance_cache = {}


def get_cached_total_balance_for_user(email: str, accounts: list) -> float:
    if email not in _user_balance_cache:
        user = get_user_by_email(email)
        target_currency = user.default_currency if user and user.default_currency else "PLN"

        total = 0.0
        for acc in accounts:
            try:
                total += convert_between_currencies(acc.balance, acc.currency, target_currency)
            except ValueError as e:
                print(f"[WARN] Pominięto konto {acc.currency}: {e}")
        _user_balance_cache[email] = total
    return _user_balance_cache[email]


def reset_user_balance(email):
    _user_balance_cache.pop(email, None)
