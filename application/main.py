from nicegui import ui
from application.views.login import login_page


def start_app():
    with ui.row():
        login_page()
    ui.run(title="Investment Advisor", port=8080)
