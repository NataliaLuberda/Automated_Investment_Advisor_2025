from dataclasses import dataclass

from nicegui import ui  # type: ignore

from application.account import get_user_accounts
from application.cqrs.commands.wyslij_przelew import WyslijPrzelew
from application.cqrs.queries.daj_historie_transakcji import (
    daj_historie_transakcji_uzytkownika,
)
from application.cqrs.queries.daj_uzytkownika import DajUzytkownika
from application.models import User, Account
from application.session import get_logged_user_email
from application.components.navbar import navbar
from application.utils.user_info import UserInfo
from application.components.transfer_form import przelew_form


@ui.page("/konto")
def konto_page():
    uzytkownik: User = get_user_details()
    rachunki_uzytkownika: list[Account] = get_user_accounts()
    user_info = UserInfo(uzytkownik, rachunki_uzytkownika)
    historia_transakcji = daj_historie_transakcji_uzytkownika(uzytkownik.id)

    with ui.column().classes("items-center w-full"):

        navbar()

        with ui.card().classes(
            "w-96 min-h-0 max-h-full flex flex-col items-left justify-left"
        ):
            with ui.card_section().classes("w-full"):
                ui.label(uzytkownik.email).classes("text-4xl w-full text-center")

            with ui.card_section().classes("w-full h-full"):

                przelew_form(user_info)

            with ui.card_section():
                with ui.tabs() as tabs:
                    historia = ui.tab("Historia")
                    rachunki = ui.tab("Moje rachunki")
                with ui.tab_panels(tabs, value=historia):
                    with ui.tab_panel(historia):
                        ui.label("Historia transakcji")

                        for t in historia_transakcji:
                            if t.id_sender == uzytkownik.id:
                                color = "red"
                                przychodzacy_wychodzacy = "wychodzący"
                            else:
                                color = "green"
                                przychodzacy_wychodzacy = "przychodzący"

                            with ui.row().classes(f"text-{color}-500 border-2"):
                                ui.label(f"Data: {t.timestamp.date()}")
                                ui.label(
                                    f"Przelew {przychodzacy_wychodzacy}: {t.amount_numeric}"
                                )

                    with ui.tab_panel(rachunki):
                        for rachunek in rachunki_uzytkownika:
                            with ui.row():
                                with ui.column().classes("w-full"):
                                    ui.label(f"Numer konta: {rachunek.id}")
                                    ui.label(
                                        f"Saldo: {rachunek.balance} {rachunek.currency}"
                                    )
                                    ui.separator()


def get_user_details() -> "User":
    uemail = get_logged_user_email()
    request = DajUzytkownika.Request(uemail)
    return DajUzytkownika.handle(request=request)
