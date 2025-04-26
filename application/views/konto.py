from nicegui import ui
from ..models_.konto_model import KontoUzytkownika
from ..utility.waluty import Waluta

@ui.page('/')
def konto_page():

    uzytkownik = KontoUzytkownika("Jan", "Kowalski", stan_konta=6534.27)
    uzytkownik.dodaj_rachunek_bankowy(Waluta.PLN, 2137.20)
    uzytkownik.dodaj_rachunek_bankowy(Waluta.USD, kwota=1776.0)
    
    _reset_styling()

    with ui.element('div').classes('w-screen h-screen flex items-center justify-center'):
        with ui.card().classes('flex flex-col items-center justify-center'):
            ui.label(uzytkownik.daj_imie_nazwisko()).classes("text-4xl")
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
                    ui.label("Twoje rachunki bankowe")
                    


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