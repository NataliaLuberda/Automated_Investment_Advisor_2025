from nicegui import ui # type: ignore
from ..models_.konto_uzytkownika_model import KontoUzytkownika
from ..models_.transakcja_model import Transakcja, TransakcjaBuilder
from ..models_.rachunek_bankowy_model import RachunekBankowy
from ..services.konto_service import KontoUzytkownikaService
from ..services.przelew_service import PrzelewService
from ..utility.waluty import Waluta
import uuid
from time import sleep

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

    PLACEHOLDER_FOR_NOW: dict[uuid, str] = {1: "Jan Joński", 2: "Artur Arktyczny", 3: "Tomasz Totalitarny"} # type: ignore
        
    transakcja_builder = TransakcjaBuilder()

    with ui.row().classes("flex justify-center items-center"):
        nowy_przelew_button = ui.button("Nowy przelew", 
            icon="add", 
            on_click=lambda: setattr(nowy_przelew_button, 'visible', False))

    with ui.column().bind_visibility_from(nowy_przelew_button, 'visible', lambda x: not x)\
            .classes("w-full border-4") as formularz:
                
        ui.select(PLACEHOLDER_FOR_NOW, label='Z rachunku:', value=1).classes('w-full').bind_value(transakcja_builder, 'od')
                
        ui.number(label="Kwota przelewu", value=0, min=0.01, max=999999999.99, step=1.0)\
        .classes('flex w-full justify-center items-center')\
        .bind_value(transakcja_builder, 'kwota')

        with ui.row().classes('flex items-center justify-center align-content'):
            czy_wziac_adresata_z_listy_kontaktow_switch = ui.switch("Adresat z kontaktów")

        adresat_selektor = ui.select(PLACEHOLDER_FOR_NOW, label='Adresat',value=1).bind_visibility_from(
            czy_wziac_adresata_z_listy_kontaktow_switch, 
            'value').classes('w-full').bind_value(transakcja_builder, 'do')

        # ui.input(label="Numer rachunku", 
        #          validation={
        #              'Zbyt długi numer rachunku.': lambda x: x is None or len(x) <= 16,
        #              'Numer rachunku może zawierać tylko cyfry.': lambda x: x is None or x.isdecimal()
        #              }).bind_visibility_from(
        #     czy_wziac_adresata_z_listy_kontaktow_switch, 
        #     'value', lambda x: not x).classes('w-full').props('type=number').bind_value(transakcja_builder, 'do')
        ui.number(label="Numer rachunku")\
        .bind_value(transakcja_builder, 'do')\
        .bind_visibility_from(czy_wziac_adresata_z_listy_kontaktow_switch, 'value', lambda x: not x)\
        .classes('w-full')
    
        ui.textarea(label="Opis przelewu", validation={"Zbyt długi opis":lambda x: len(x) <= TransakcjaBuilder.DLUGOSC_OPISU_LIMIT})\
            .classes('w-full')\
            .bind_value(transakcja_builder, 'opis')\
            .props(f"maxlength={TransakcjaBuilder.DLUGOSC_OPISU_LIMIT}")
        
            
        ui.button("Wyślij", 
                    icon="send", 
                    on_click=lambda: _wyslij_przelew_onclick(
                        nowy_przelew_button, 
                        transakcja_builder.with_time_now().build()
                        ))
            
async def _wyslij_przelew_onclick(element_to_toggle_visible , transakcja: Transakcja) -> bool:
    przelew_service = PrzelewService()
    przelew_response = await przelew_service.handle(przelew_service.Request(transakcja=transakcja))
    if przelew_response.status_ok:
        ui.notify(f"Wysłano przelew! 🚀 {transakcja}", type="positive")
        setattr(element_to_toggle_visible, 'visible', True)
        return True
    else:
        ui.notify(transakcja, type="negative")
        return False