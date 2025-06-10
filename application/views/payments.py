from nicegui import ui

from application.account import get_user_accounts
from application.components.navbar import navbar
from application.components.payment_form import PaymentForm
from application.cqrs.queries.get_transaction_history import get_accounts_transaction_history
from application.cqrs.queries.get_user import GetUser
from application.models import User, Account
from application.session import get_logged_user_email
from application.utils.user_info import UserInfo


@ui.page("/payments")
def payment_page():
    with ui.column().classes("items-center w-full"):
        navbar()

        try:
            user: User = get_user_details()
            user_accounts: list[Account] = get_user_accounts()
            user_info = UserInfo(user, user_accounts)

            with ui.card().classes(
                    "w-full max-w-4xl flex flex-col p-6 bg-blue-500 text-white rounded-xl shadow-md"
            ):
                with ui.card_section().classes("w-full"):
                    ui.label(f"Witaj, {user.email}!").classes(
                        "text-4xl w-full text-center"
                    )

                PaymentForm(user_info)

                search_query = ui.input(
                    label="Wyszukaj konto po walucie lub ID"
                ).classes("my-4 w-full text-white placeholder-white").props("color=white")

                result_container = ui.element().classes("w-full")

                def show_accounts():
                    result_container.clear()
                    query = (search_query.value or "").strip().lower()

                    filtered_accounts = [
                        acc for acc in user_accounts
                        if not query or query in acc.currency.lower() or query in str(acc.id)
                    ]

                    with result_container:
                        with ui.scroll_area().classes(
                                "max-h-96 w-full p-2 bg-white text-black rounded-lg shadow-inner"):
                            if not filtered_accounts:
                                ui.label("Brak pasujących kont.").classes(
                                    "text-center text-gray-500 italic py-4"
                                )
                                return

                            for account in filtered_accounts:
                                with ui.card().classes(
                                        "bg-blue-100 text-black w-full my-2 p-2 rounded-lg shadow-sm"
                                ):
                                    ui.label(
                                        f"Historia transakcji: {account.currency} ({account.id})"
                                    ).classes("font-bold text-md")

                                    transactions = get_accounts_transaction_history(account.id)
                                    if not transactions:
                                        ui.label("Brak transakcji.").classes(
                                            "text-sm italic text-gray-500"
                                        )
                                    else:
                                        with ui.scroll_area().classes(
                                                "max-h-40 w-full mt-1"
                                        ):
                                            for t in transactions:
                                                direction = (
                                                    "⬆️ Wysłano"
                                                    if t.source_account_id == account.id
                                                    else "⬇️ Otrzymano"
                                                )
                                                amount = f"{t.amount_numeric:.2f} {account.currency}"
                                                counterparty_id = (
                                                    t.target_account_id
                                                    if direction == "⬆️ Wysłano"
                                                    else t.source_account_id
                                                )
                                                description = t.description or ""
                                                ui.label(
                                                    f"{direction}: {amount} do/od: {counterparty_id} | Opis: {description}"
                                                ).classes("text-sm my-1")

                search_query.on("update:model-value", lambda _: show_accounts())
                show_accounts()

        except Exception as e:
            ui.label("Wystąpił błąd. Spróbuj ponownie później.").classes("text-red-700")
            ui.notify(f"Błąd: {e}", type="negative", timeout=5000)


def get_user_details() -> User:
    user_email = get_logged_user_email()
    request = GetUser.Request(user_email)
    user = GetUser.handle(request=request)

    if user is None:
        raise ValueError("Nie znaleziono użytkownika")

    return user
