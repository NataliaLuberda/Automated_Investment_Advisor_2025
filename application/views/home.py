from random import choice

from nicegui import ui

from application.account import get_user_accounts
from application.auth import get_user_by_email
from application.cqrs.queries.get_transaction_history import get_accounts_transaction_history
from application.session import logout_user, get_logged_user_email
from application.utils.catched_total_balance import get_cached_total_balance_for_user
from application.utils.currency import fetch_currency_codes
from application.utils.tips import financial_tips
from application.components.navbar import navbar


@ui.page("/home")
def home_page():
    user_name = get_logged_user_email()

    accounts = get_user_accounts() or []
    user = get_user_by_email(user_name)
    default_currency = (
        user.default_currency if user and user.default_currency else "PLN"
    )
    total_balance = get_cached_total_balance_for_user(user_name, accounts)
    transactions = []
    for acc in accounts:
        transactions += get_accounts_transaction_history(acc.id)

    income = sum(t.amount_numeric for t in transactions if t.target_account_id in accounts)
    expense = sum(t.amount_numeric for t in transactions if t.source_account_id in accounts)
    savings = max(0, income - expense)

    currency_wallet = {}
    for acc in accounts:
        currency_wallet[acc.currency] = (
            currency_wallet.get(acc.currency, 0) + acc.balance
        )

    with ui.column().classes("items-center w-full"):

        navbar()

        ui.separator().classes("my-4")

        with ui.card().classes(
            "w-full max-w-4xl p-6 bg-green-50 rounded-lg shadow flex items-center gap-4 mb-6"
        ) as tip_card:
            ui.label("💡").classes("text-4xl")
            tip_label = ui.label("").classes("text-md font-medium text-green-900")

            def update_tip():
                tip_label.text = choice(financial_tips)

            update_tip()
            ui.timer(interval=10.0, callback=update_tip)

        card_classes = "w-full max-w-md p-6 bg-blue-500 text-white rounded-xl shadow-md hover:shadow-xl transition-transform duration-300 hover:scale-105"
        label_header = "text-lg font-semibold mb-2"
        label_value = "text-4xl font-bold"

        with ui.row().classes(
            "w-full max-w-6xl gap-12 justify-center items-start flex-wrap"
        ):

            with ui.card().classes(card_classes):
                ui.label("Saldo główne").classes(label_header)
                ui.label(f"{total_balance:.2f} {default_currency}").classes(
                    label_value + " text-green-200"
                )

                ui.label("Oszczędności").classes(label_header + " mt-4")
                ui.label(f"{savings:.2f} {default_currency}").classes(
                    label_value + " text-orange-200"
                )

            with ui.card().classes(card_classes):
                ui.label("Portfel walutowy").classes(label_header)

                if currency_wallet:
                    with ui.row().classes("justify-around flex-wrap"):
                        for currency, amount in currency_wallet.items():
                            with ui.column().classes("items-center m-2"):
                                ui.label(currency).classes(
                                    "text-white font-bold text-xl"
                                )
                                ui.label(f"{amount:.2f}").classes("text-white")
                else:
                    ui.label("Brak dostępnych walut").classes("italic text-white")

        with ui.card().classes(card_classes + " mt-6 max-w-4xl"):
            ui.label("Wybierz konto domyślne:").classes(label_header)
            currencies = fetch_currency_codes()

            if accounts:
                options = {
                    f"{code} - {currencies.get(code, code)}": code
                    for code in currencies
                }
                default_label = next(
                    (
                        label
                        for label, curr in options.items()
                        if curr == default_currency
                    ),
                    None,
                )
                with ui.row().classes("item-end gap-4 mt-2"):

                    default_account_select = ui.select(
                        options, label="Konto domyślne", value=default_label
                    ).classes("w-60 bg-skyblue text-blue-600 font-bold")

                from application.account import update_default_account_currency

                def set_default():
                    selected_label = default_account_select.value
                    selected_currency = options.get(selected_label)
                    if selected_currency:
                        result = update_default_account_currency(selected_currency)
                        ui.notify(result, timeout=3000)
                        ui.navigate.reload()
                    else:
                        ui.notify(
                            "Wybierz konto przed zapisaniem",
                            type="warning",
                            timeout=3000,
                        )

                ui.button("Ustaw jako domyślne", on_click=set_default).classes(
                    "bg-lightblue text-blue-600 font-bold hover:bg-blue-100"
                )
            else:
                ui.label("Nie masz żadnych kont").classes("italic text-white mt-4")
