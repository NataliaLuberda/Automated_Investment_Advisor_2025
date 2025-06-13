from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional
import requests
from datetime import datetime, timedelta
from .error_handler import ApplicationError
from .config import config

class CurrencyConverter:
    _instance = None
    _rates: Dict[str, Decimal] = {}
    _last_update: Optional[datetime] = None
    _cache_duration = timedelta(hours=1)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrencyConverter, cls).__new__(cls)
        return cls._instance

    def _fetch_exchange_rates(self):
        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/PLN')
            if response.status_code != 200:
                raise ApplicationError("Nie udało się pobrać kursów walut")
            
            data = response.json()
            self._rates = {
                currency: Decimal(str(rate))
                for currency, rate in data['rates'].items()
                if currency in config.supported_currencies
            }
            self._last_update = datetime.now()
        except requests.RequestException as e:
            raise ApplicationError(f"Błąd podczas pobierania kursów walut: {str(e)}")

    def _ensure_rates_updated(self):
        if (self._last_update is None or 
            datetime.now() - self._last_update > self._cache_duration):
            self._fetch_exchange_rates()

    def convert(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        if from_currency == to_currency:
            return amount

        self._ensure_rates_updated()

        if from_currency not in self._rates or to_currency not in self._rates:
            raise ApplicationError(f"Nieobsługiwana waluta: {from_currency} lub {to_currency}")

        if from_currency == 'PLN':
            return (amount / self._rates[to_currency]).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        elif to_currency == 'PLN':
            return (amount * self._rates[from_currency]).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        else:
            pln_amount = amount * self._rates[from_currency]
            return (pln_amount / self._rates[to_currency]).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

    def format_amount(self, amount: Decimal, currency: str) -> str:
        symbol = config.currency_symbols.get(currency, currency)
        return f"{amount:,.2f} {symbol}"

converter = CurrencyConverter()
