from nicegui import ui
from ..models_.konto_model import KontoUzytkownika, Transakcja, TransakcjaBuilder
from ..utility.waluty import Waluta
import uuid

@ui.page('/')
def konto_page():
    uzytkownik = KontoUzytkownika("Jan", "Kowalski")
    uzytkownik.dodaj_rachunek_bankowy(Waluta.PLN, kwota=2137.20)
    uzytkownik.dodaj_rachunek_bankowy(Waluta.USD, kwota=1776.0)
    
    _reset_styling()

    with ui.element('div').classes('w-screen h-screen flex items-center justify-center'):

        with ui.card().classes('w-96 min-h-0 max-h-full flex flex-col items-left justify-left'):

            with ui.card_section().classes("w-full"):
                ui.label(uzytkownik.daj_imie_nazwisko()).classes("text-4xl w-full text-center")

            with ui.card_section().classes("w-full h-full"):
                pole_przelewu()

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
                        for rachunek in uzytkownik.daj_rachunki_uzytkownika():
                            with ui.row():
                                ui.label(f"Stan konta: {rachunek.kwota} {rachunek._waluta.name}")
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
    
def pole_przelewu() -> None:

    szablon_transakcji = TransakcjaBuilder()

    with ui.row().classes("flex justify-center items-center"):
        nowy_przelew_button = ui.button(
            "Nowy przelew", 
            icon="new", 
            on_click=lambda : setattr(nowy_przelew_button, 'visible', False))

        with ui.column().bind_visibility_from(nowy_przelew_button, 'visible', lambda x: not x) as formularz:
            ui.number(label="Kwota przelewu", value=0, min=0.01, max=999999999.99, step=1.0)\
            .classes('w-full')\
            .bind_value(szablon_transakcji, '_kwota')

            with ui.row().classes('flex align-center items-center border'):
                ui.label("Adresat:")
                PLACEHOLDER_FOR_NOW = {1: "Jan Joński", 2: "Artur Arktyczny", 3: "Tomasz Totalitarny"}
                czy_wziac_adresata_z_listy_kontaktow_switch = ui.switch("Z kontaktów")

            ui.select(PLACEHOLDER_FOR_NOW, value=1).bind_visibility_from(
                czy_wziac_adresata_z_listy_kontaktow_switch, 
                'value').classes('w-full')

            ui.input(label="Numer rachunku").bind_visibility_from(
                czy_wziac_adresata_z_listy_kontaktow_switch, 
                'value', lambda x: not x).classes('w-full')
            
            ui.textarea(label="Opis przelewu").classes('w-full')
            przycisk_wyslij = ui.button("Wyślij", icon="send", on_click=lambda: setattr(nowy_przelew_button, 'visible', True))