import requests

API_KEY = "cur_live_WllS2ns9qh9K1PIRxkpLkFoYgYc6shSXDvZBnO51"


def convert_between_currencies(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return round(amount, 2)

    rates = get_currencyapi_rates(base_currency=from_currency, symbols=[to_currency])
    converted = amount * rates[to_currency]
    return round(converted, 2)


def get_currencyapi_rates(base_currency: str = "PLN", symbols: list[str] = None) -> dict:
    if symbols is None:
        symbols = ["USD", "EUR", "GBP", "CAD"]

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
    return rates


def fetch_currency_codes():
    url = "https://openexchangerates.org/api/currencies.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except Exception:
        return {}
