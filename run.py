from nicegui import ui
from application.services.database import init_db
from application.views.login import login_page
from application.views.accounts import account_page
from application.views.register import register_page
from application.views.home import home_page
from application.views.payments import payment_page
from application.services.database import init_db
from application.views.transaction import transaction_page


def start_app():
    ui.run(title="Investment Advisor", port=8080, storage_secret="super-secret-key")


if __name__ in {"__main__", "__mp_main__"}:
    init_db()
    start_app()
