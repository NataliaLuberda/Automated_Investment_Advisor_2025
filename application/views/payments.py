from nicegui import ui  # type: ignore

from application.account import get_user_accounts
from application.cqrs.queries.get_user import GetUser
from application.models import User, Account
from application.session import get_logged_user_email
from application.components.navbar import navbar
from application.utils.user_info import UserInfo
from application.components.payment_form import PaymentForm


@ui.page("/payments")
def payment_page():

    with ui.column().classes("items-center w-full"):

        navbar()

        try:

            user: User = get_user_details()
            user_accounts: list[Account] = get_user_accounts()
            user_info = UserInfo(user, user_accounts)

            with ui.card().classes(
                "w-1/2 min-h-0 max-h-full flex flex-col items-left justify-left p-8 bg-blue-500 text-white rounded-xl shadow-md"
            ):
                with ui.card_section().classes("w-full"):
                    ui.label(f"Witaj, {user.email}!").classes(
                        "text-4xl w-full text-center"
                    )

                with ui.card_section().classes("w-full h-full"):

                    PaymentForm(user_info)

        except Exception as e:
            ui.label("Wystąpił błąd. Spróbuj ponownie później.")
            ui.notify(f"Parametry wyjątku: {e}.", type="negative")


def get_user_details() -> "User":
    user_email = get_logged_user_email()
    request = GetUser.Request(user_email)
    user: User = GetUser.handle(request=request)

    if user is None:
        raise ValueError("Nie znaleziono użytkownika")

    return user
