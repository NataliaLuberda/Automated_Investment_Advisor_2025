from application.utils.currency import convert_between_currencies

_user_balance_cache = {}


def get_cached_total_balance_for_user(email: str, accounts: list) -> float:
    if email not in _user_balance_cache:
        total = 0.0
        for acc in accounts:
            try:
                total += convert_between_currencies(acc.balance, acc.currency, "PLN")
            except ValueError as e:
                print(f"[WARN] Pominięto konto {acc.currency}: {e}")
        _user_balance_cache[email] = total
    return _user_balance_cache[email]


def reset_user_balance(email):
    _user_balance_cache.pop(email, None)
