from dataclasses import dataclass

from nicegui import ui  # type: ignore

from application.account import get_user_accounts
from application.cqrs.queries.daj_historie_transakcji import (
    daj_historie_transakcji_uzytkownika,
)
from application.cqrs.queries.daj_uzytkownika import DajUzytkownika
from application.models import User, Account
from application.session import get_logged_user_email
from application.components.navbar import navbar
from application.utils.user_info import UserInfo
from application.components.przelew_form import PrzelewForm


@ui.page("/konto")
def konto_page():

    with ui.column().classes("items-center w-full"):

        navbar()

        try:

            uzytkownik: User = get_user_details()
            rachunki_uzytkownika: list[Account] = get_user_accounts()
            user_info = UserInfo(uzytkownik, rachunki_uzytkownika)

            with ui.card().classes(
                "w-1/2 min-h-0 max-h-full flex flex-col items-left justify-left p-8 bg-blue-500 text-white rounded-xl shadow-md"
            ):
                with ui.card_section().classes("w-full"):
                    ui.label(f"Witaj, {uzytkownik.email}!").classes(
                        "text-4xl w-full text-center"
                    )

                with ui.card_section().classes("w-full h-full"):

                    PrzelewForm(user_info)

        except Exception as e:
            ui.label("Wystąpił błąd. Spróbuj ponownie później.")
            ui.notify(f"Parametry wyjątku: {e}.", type="negative")


def get_user_details() -> "User":
    uemail = get_logged_user_email()
    request = DajUzytkownika.Request(uemail)
    uzytkownik: User = DajUzytkownika.handle(request=request)

    if uzytkownik is None:
        raise ValueError("Nie znaleziono użytkownika")

    return uzytkownik
