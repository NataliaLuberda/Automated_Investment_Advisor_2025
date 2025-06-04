from nicegui import ui  # type: ignore
from application.cqrs.commands.wyslij_przelew import WyslijPrzelew
from application.cqrs.queries.daj_uzytkownika import DajUzytkownika
from application.session import get_logged_user_email
from application.models import User, Account, Transakcja
from application.account import get_user_accounts
from dataclasses import dataclass

@ui.page('/konto')
def konto_page():
    
    uzytkownik: User = get_user_details()
    rachunki_uzytkownika: list[Account] = get_user_accounts()
    user_info = UserInfo(uzytkownik, rachunki_uzytkownika)
    
    _reset_styling()

    with ui.element('div').classes('w-screen h-screen flex items-center justify-center'):
        with ui.card().classes('w-96 min-h-0 max-h-full flex flex-col items-left justify-left'):
            with ui.card_section().classes("w-full"):
                ui.label(uzytkownik.email).classes("text-4xl w-full text-center")

            with ui.card_section().classes("w-full h-full"):
                pole_przelewu(user_info)

            with ui.card_section():
                with ui.tabs() as tabs:
                    wydatki = ui.tab("Wydatki")
                    historia = ui.tab("Historia")
                    rachunki = ui.tab("Moje rachunki")
                with ui.tab_panels(tabs, value=wydatki):
                    with ui.tab_panel(wydatki):
                        ui.label("Twoja historia wydatków")
                    with ui.tab_panel(historia):
                        ui.label("Twoja historia wydatków")
                    with ui.tab_panel(rachunki):
                        for rachunek in rachunki_uzytkownika:
                            with ui.row():
                                ui.label(f"Stan konta: {rachunek.balance} {rachunek.currency}")
                                ui.separator()


def _reset_styling() -> None:
    ui.add_head_html('''
        <style>
            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
        </style>
        ''')


def pole_przelewu(user_info: 'UserInfo') -> None:

    transakcja = Transakcja()

    with ui.row().classes("flex justify-center items-center"):
        nowy_przelew_button = ui.button("Nowy przelew",
                                        icon="add",
                                        on_click=lambda: setattr(nowy_przelew_button, 'visible', False))

    with ui.column().bind_visibility_from(nowy_przelew_button, 'visible', lambda x: not x) \
            .classes("w-full border-4"):
        
        select_options = {
            acc.id: f'{acc.currency}'
            for acc in user_info.account_list
        }
        
        ui.select(
            options=select_options,
            label='Z rachunku:',
            value=transakcja.id_sender
        ).classes('w-full').bind_value(transakcja, 'id_sender')

        ui.number(label="Kwota przelewu", value=0, min=0.01, max=999999999.99, step=1.0) \
            .classes('flex w-full justify-center items-center') \
            .bind_value(transakcja, 'amount_numeric')

        ui.number(label="Numer rachunku adresata") \
            .bind_value(transakcja, 'id_receiver') \
            .classes('w-full')

        ui.textarea(label="Opis przelewu",
                    validation={"Zbyt długi opis": lambda x: len(x or '') <= transakcja.MAX_DESC_LENGTH}) \
            .classes('w-full') \
            .bind_value(transakcja, 'description') \
            .props(f"maxlength={transakcja.MAX_DESC_LENGTH}")

        ui.button("Wyślij",
                  icon="send",
                  on_click=lambda: _wyslij_przelew_onclick(
                      nowy_przelew_button,
                      transakcja
                  ))


async def _wyslij_przelew_onclick(element_to_toggle_visible, transakcja: Transakcja) -> None:
    request = WyslijPrzelew.Request(
        id_nadawcy=transakcja.id_sender,
        id_adresata=transakcja.id_receiver,
        kwota=transakcja.amount_numeric,
        opis=transakcja.description
    )
    try:
        await WyslijPrzelew.handle(request)
        ui.notify(f"Wysłano przelew! 🚀", type="positive")
        setattr(element_to_toggle_visible, 'visible', True)
        
    except Exception as e:
        ui.notify(f"Wysyłka nie powiodła się: {e}", type="negative")

def get_user_details() -> 'User':
    uemail = get_logged_user_email()
    request = DajUzytkownika.Request(uemail)
    return DajUzytkownika.handle(request=request)

@dataclass
class UserInfo:
    user: User
    account_list: list[Account]