from nicegui import ui
#from ..models.konto_model import Konto

@ui.page('/')
def konto_page():

    #uzytkownik = Konto("Jan", "Kowalski")
    
    _reset_styling()

    with ui.element('div').classes('w-screen h-screen flex items-center justify-center'):
        with ui.card().classes('flex flex-col items-center justify-center'):
            ui.label(f"Konto użytkownika {"Jan Kowalski"}").classes("text-4xl")
            with ui.card_section():
                with ui.row():
                    ui.label("sigma")
                    ui.label("sigma2")
                    


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