import requests
import time

_currency_cache = None
_currency_cache_time = 0
_CURRENCY_CODES_CACHE_TTL = 60 * 60 * 24 * 7  # 1 tydzień
_rates_cache = {}  # klucz: (base_currency, tuple(symbols)), wartość: (czas, rates)
_RATES_CACHE_TTL = 60 * 60 * 24  # np. 1 dzień

API_KEY = "cur_live_WllS2ns9qh9K1PIRxkpLkFoYgYc6shSXDvZBnO51"


def convert_between_currencies(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return round(amount, 2)

    rates = get_currencyapi_rates(base_currency=from_currency, symbols=[to_currency])
    converted = amount * rates[to_currency]
    return round(converted, 2)


def get_currencyapi_rates(base_currency: str = "PLN", symbols: list[str] = None) -> dict:
    global _rates_cache
    if symbols is None:
        symbols = ["USD", "EUR", "GBP", "CAD"]

    symbols_tuple = tuple(symbols)
    cache_key = (base_currency, symbols_tuple)
    now = time.time()

    if cache_key in _rates_cache:
        cached_time, rates = _rates_cache[cache_key]
        if now - cached_time < _RATES_CACHE_TTL:
            return rates

    symbols_param = ",".join(symbols)
    url = f"https://api.currencyapi.com/v3/latest?apikey={API_KEY}&base_currency={base_currency}&currencies={symbols_param}"

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

    _rates_cache[cache_key] = (now, rates)
    return rates


def fetch_currency_codes():
    global _currency_cache, _currency_cache_time
    now = time.time()

    if _currency_cache and (now - _currency_cache_time) < _CURRENCY_CODES_CACHE_TTL:
        return _currency_cache

    url = "https://openexchangerates.org/api/currencies.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            _currency_cache = response.json()
            _currency_cache_time = now
            return _currency_cache
        else:
            return _currency_cache or {}
    except Exception:
        return _currency_cache or {}
