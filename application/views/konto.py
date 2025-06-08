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
            historia_transakcji = daj_historie_transakcji_uzytkownika(uzytkownik.id)

            with ui.card().classes(
                "w-50 min-h-0 max-h-full flex flex-col items-left justify-left"
            ):
                with ui.card_section().classes("w-full"):
                    ui.label(uzytkownik.email).classes("text-4xl w-full text-center")

                with ui.card_section().classes("w-full h-full"):

                    PrzelewForm(user_info)

                with ui.card_section():
                    with ui.tabs() as tabs:
                        historia = ui.tab("Historia")
                        rachunki = ui.tab("Moje rachunki")
                    with ui.tab_panels(tabs, value=historia).classes("w-full"):

                        with ui.tab_panel(historia):

                            with ui.list().props("bordered separator"):

                                ui.item_label("Historia transakcji").props(
                                    "header"
                                ).classes("text-bold")
                                ui.separator()

                                for t in historia_transakcji:
                                    if t.id_sender == uzytkownik.id:
                                        color = "red"
                                        przychodzacy_wychodzacy = "wychodzący"
                                    else:
                                        color = "green"
                                        przychodzacy_wychodzacy = "przychodzący"

                                    with ui.item():
                                        with ui.row().classes(f"text-{color}-500"):
                                            ui.item_label(f"Data: {t.timestamp.date()}")
                                            ui.item_label(
                                                f"Przelew {przychodzacy_wychodzacy}: {t.amount_numeric}"
                                            )
                                            with ui.row().classes(f"text-black"):
                                                ui.item_label(
                                                    f"Z rachunku: {t.id_sender}"
                                                )
                                                ui.item_label(
                                                    f"Na rachunek: {t.id_receiver}"
                                                )

                        with ui.tab_panel(rachunki):

                            with ui.list().props("bordered separator"):
                                ui.item_label("Moje rachunki").props("header").classes(
                                    "text-bold"
                                )
                                ui.separator()

                                for rachunek in rachunki_uzytkownika:
                                    with ui.item():
                                        with ui.column().classes("w-full"):
                                            ui.item_label(f"Nr. konta: {rachunek.id}")
                                            ui.item_label(
                                                f"Saldo: {rachunek.balance} {rachunek.currency}"
                                            )
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
