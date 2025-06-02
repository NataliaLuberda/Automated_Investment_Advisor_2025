from nicegui import ui

from application.views.login import login_page


def start_app():
    with ui.row():
        login_page()
    ui.run(
        title="Automated Investment Advisor",
        port=8080,
        storage_secret="super-secret-key"
    )
