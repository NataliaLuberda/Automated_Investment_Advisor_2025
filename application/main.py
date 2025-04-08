from nicegui import ui
from application.views.login import login_page


def start_app():
    with ui.row():
        login_page()
    ui.run(title="Gimme your money", port=8080)
