from application.database import init_db
import application.views.login
import application.views.register
import application.views.home
import application.views.konto
import application.views.accounts
from nicegui import ui


def start_app():
    ui.run(
        title="Investment Advisor",
        port=8080,
        storage_secret="super-secret-key"
    )


if __name__ in {"__main__", "__mp_main__"}:
    init_db()
    start_app()
