from nicegui import ui
from sqlalchemy.orm import Session
from application.models import User, Account
from application.auth import get_user_by_email
from application.session import get_logged_user_email
from application.account import get_user_accounts
from application.cqrs.queries.get_transaction_history import (
    get_accounts_transaction_history,
)
from application.components.navbar import navbar
from datetime import datetime, timedelta


@ui.page("/transaction")
def transaction_page():

    navbar()

    user_email = get_logged_user_email()
    user: User = get_user_by_email(user_email)

    ui.label(f"🏠 Przegląd Twojego budżetu, {user_email}").classes("text-h4")
    ui.button("Wyloguj", on_click=lambda: ui.navigate.to("/login"))

    user_accounts = get_user_accounts()

    ui.label(f"Witaj, {user.email}!").classes("text-2xl font-bold mt-4")
    default_currency = (
        user.default_currency if user and user.default_currency else "PLN"
    )
    default_account: Account = next(
        (acc for acc in user_accounts if acc.currency == default_currency), None
    )

    main_balance: Account = default_account.balance

    savings = 1500

    with ui.row().classes("w-full max-w-4xl justify-center gap-8"):
        with ui.card().classes("w-full max-w-sm bg-blue-50"):
            ui.label("Saldo główne").classes("text-lg text-gray-600")
            ui.label(f"{main_balance:.2f} {user.default_currency or 'PLN'}").classes(
                "text-3xl font-bold text-green-600"
            )

        with ui.card().classes("w-full max-w-sm bg-yellow-50"):
            ui.label("Oszczędności").classes("text-lg text-gray-600")
            ui.label(f"{savings:.2f} {user.default_currency or 'PLN'}").classes(
                "text-3xl font-bold text-orange-500"
            )

    ui.label("Historia transakcji").classes("text-xl font-semibold mt-6")

    transactions = (
        get_accounts_transaction_history(user_accounts[0].id)
        if user_accounts and len(user_accounts) > 0
        else []
    )
    account_ids = [acc.id for acc in user_accounts]

    #Date filter
    today = datetime.today().date()
    thirty_days_ago = today - timedelta(days=30)

    with ui.row().classes("w-full justify-center mt-4"):
        with ui.row().classes("gap-4 items-center"):
            with ui.column():
                ui.label("Od")
                date_from = ui.date(value=thirty_days_ago)
            with ui.column():
                ui.label("Do")
                date_to = ui.date(value=today)
            filter_button = ui.button("Filtruj")


    transaction_container = ui.column().classes("items-center w-full mt-4")

    def render_transactions(filtered_tx):
        transaction_container.clear()
        with transaction_container:
            with ui.list().props("bordered separator").classes("w-full max-w-3xl"):
                ui.item_label("Transakcje").props("header").classes("text-bold")
                ui.separator()
                for trans in filtered_tx:
                    is_income = trans.target_account_id in account_ids
                    amount = trans.amount_numeric if is_income else -trans.amount_numeric
                    kolor = "text-green-600" if amount >= 0 else "text-red-600"

                    with ui.item():
                        with ui.item_section().props("avatar"):
                            ui.icon("attach_money")
                        with ui.item_section():
                            ui.item_label(trans.description)
                            ui.item_label(trans.timestamp.strftime("%Y-%m-%d %H:%M")).props(
                                "caption"
                            )
                        with ui.item_section().props("side"):
                            ui.item_label(f"{amount:.2f}").classes(f"font-semibold {kolor}")
                        with ui.item_section().props("side"):
                            ui.item_label(user.default_currency or "PLN").classes(
                                "text-gray-500 text-sm"
                            )

    def filter_transactions():
        start_raw = date_from.value
        end_raw = date_to.value

        if not start_raw or not end_raw:
            return transactions

        # Konwersja do typu datetime.date (jeśli nie jest)
        if isinstance(start_raw, str):
            start = datetime.strptime(start_raw, "%Y-%m-%d").date()
        else:
            start = start_raw

        if isinstance(end_raw, str):
            end = datetime.strptime(end_raw, "%Y-%m-%d").date()
        else:
            end = end_raw

        return [
            t for t in transactions
            if start <= t.timestamp.date() <= end
        ]




    #Summary chart for specified date
    summary_chart = ui.echart(
        {
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "data": ["Dochody", "Wydatki"],
                "axisLabel": {"color": "gray"},
            },
            "yAxis": {"type": "value", "axisLabel": {"color": "gray"}},
            "series": [
                {
                    "type": "bar",
                    "data": [],
                    "label": {"show": True, "position": "top", "color": "black"},
                }
            ],
        }
    )

    def update_summary_chart(filtered_tx):
        income = sum(
            t.amount_numeric for t in filtered_tx if t.target_account_id in account_ids
        )
        expense = sum(
            t.amount_numeric for t in filtered_tx if t.source_account_id in account_ids
        )
        summary_chart.options["series"][0]["data"] = [
            {"value": income, "itemStyle": {"color": "#4caf50"}},
            {"value": expense, "itemStyle": {"color": "#f44336"}},
        ]
        summary_chart.update()

    
    def on_filter_click():
        filtered = filter_transactions()
        render_transactions(filtered)
        update_summary_chart(filtered)

    filter_button.on("click", on_filter_click)
    



    filtered_initial = filter_transactions()
    render_transactions(filtered_initial)
    update_summary_chart(filtered_initial)

    with ui.row().classes("w-full justify-center"):
        ui.button("🔄 Odśwież wykres", on_click=lambda: update_summary_chart(filter_transactions())).classes("mt-4")

