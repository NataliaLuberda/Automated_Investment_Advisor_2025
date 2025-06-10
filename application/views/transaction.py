from nicegui import ui
from datetime import datetime, timedelta, date
from application.models import User
from application.auth import get_user_by_email
from application.session import get_logged_user_email
from application.account import get_user_accounts
from application.cqrs.queries.get_transaction_history import get_accounts_transaction_history
from application.components.navbar import navbar
import csv
import io


@ui.page("/transaction")
def transaction_page():
    navbar()

    user_email = get_logged_user_email()
    user: User = get_user_by_email(user_email)
    user_accounts = get_user_accounts()
    account_ids = [acc.id for acc in user_accounts] if user_accounts else []

    default_currency = user.default_currency if user and user.default_currency else "PLN"
    default_account = next((acc for acc in user_accounts if acc.currency == default_currency), None)
    main_balance = default_account.balance if default_account else 0
    transactions = get_accounts_transaction_history(user_accounts[0].id) if user_accounts else []
    savings = sum(t.amount_numeric for t in transactions if t.target_account_id in account_ids) - \
              sum(t.amount_numeric for t in transactions if t.source_account_id in account_ids)

    summary_chart_ref = {'chart': None}
    income_label_ref = {'label': None}
    expense_label_ref = {'label': None}
    balance_label_ref = {'label': None}

    def update_summary_chart():
        nonlocal transactions

        income = sum(t.amount_numeric for t in transactions if t.target_account_id in account_ids)
        expense = sum(t.amount_numeric for t in transactions if t.source_account_id in account_ids)
        balance = float(income) - float(expense)

        chart_options = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {"type": "category", "data": ["Wpływy", "Wydatki"],
                      "axisLabel": {"color": "#666", "fontSize": 12}},
            "yAxis": {"type": "value", "axisLabel": {"color": "#666", "fontSize": 12},
                      "splitLine": {"lineStyle": {"color": "#eee"}}},
            "series": [{
                "type": "bar",
                "data": [
                    {"value": float(income), "itemStyle": {"color": "#4CAF50"}},
                    {"value": float(expense), "itemStyle": {"color": "#F44336"}},
                ],
                "label": {
                    "show": False  # 👈 wyłącza etykiety nad słupkami
                },
                "barWidth": "40%",
            }],
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        }

        chart = summary_chart_ref['chart']
        if chart:
            chart.options.clear()
            chart.options.update(chart_options)
            chart.update()

        income_label = income_label_ref['label']
        expense_label = expense_label_ref['label']
        balance_label = balance_label_ref['label']
        if income_label and expense_label and balance_label:
            income_label.text = f"+{income:.2f}"
            expense_label.text = f"-{expense:.2f}"
            balance_label.text = f"{balance:+.2f}"
            balance_label.classes(replace=f"text-sm font-bold {'text-green-600' if balance >= 0 else 'text-red-600'}")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Historia transakcji").classes("text-2xl font-bold text-blue-800")
            with ui.row().classes("gap-3"):
                with ui.card().classes("p-2 px-3 bg-blue-50 rounded-lg"):
                    ui.label(f"{main_balance:.2f} {default_currency}").classes("text-sm font-bold text-blue-800")
                    ui.label("Saldo").classes("text-xs text-blue-600")
                with ui.card().classes("p-2 px-3 bg-green-50 rounded-lg"):
                    ui.label(f"{savings:.2f} {default_currency}").classes("text-sm font-bold text-green-800")
                    ui.label("Oszczędności").classes("text-xs text-green-600")

        with ui.row().classes("w-full gap-4 mt-4 items-start no-wrap"):

            with ui.column().classes("bg-gray-50 p-3 rounded-lg border min-w-[280px] sticky top-4"):
                today = datetime.today().date()
                thirty_days_ago = today - timedelta(days=30)

                ui.label("Filtruj transakcje").classes("font-medium text-gray-700 mb-2")
                date_from = ui.date(value=thirty_days_ago).props("dense bordered").classes("w-full")
                date_to = ui.date(value=today).props("dense bordered").classes("w-full")

                def to_date(value):
                    if isinstance(value, str):
                        return datetime.strptime(value, "%Y-%m-%d").date()
                    elif isinstance(value, datetime):
                        return value.date()
                    elif isinstance(value, date):
                        return value
                    raise ValueError("Nieobsługiwany format daty")

                def apply_filters():
                    nonlocal transactions

                    start_date = to_date(date_from.value)
                    end_date = to_date(date_to.value)

                    filtered = get_accounts_transaction_history(user_accounts[0].id) if user_accounts else []
                    filtered = [t for t in filtered if start_date <= t.timestamp.date() <= end_date]

                    transactions = filtered
                    transaction_container.clear()
                    render_transactions()
                    update_summary_chart()

                def export_to_csv():
                    output = io.StringIO()
                    writer = csv.writer(output)
                    writer.writerow(['Data', 'Opis', 'Kwota', 'Typ'])
                    for t in transactions:
                        writer.writerow([
                            t.timestamp.strftime("%Y-%m-%d %H:%M"),
                            t.description,
                            f"{t.amount_numeric:.2f}",
                            "Wpływ" if t.target_account_id in account_ids else "Wydatek"
                        ])
                    ui.download(output.getvalue().encode(), filename='transakcje.csv')

                date_from.on("update:model-value", lambda e: apply_filters())
                date_to.on("update:model-value", lambda e: apply_filters())

                ui.button("Eksportuj do CSV", icon="download", on_click=export_to_csv) \
                    .classes("w-full mt-2 bg-green-500 text-white py-1 h-8")

            with ui.column().classes("flex-1 bg-white p-0 rounded-lg border overflow-hidden"):
                transaction_container = ui.column().classes("w-full")

                def render_transactions():
                    with transaction_container:
                        with ui.row().classes("bg-gray-100 p-2 border-b items-center justify-between"):
                            ui.label("Ostatnie transakcje").classes("font-medium text-gray-700")
                            ui.label(f"Liczba: {len(transactions)}").classes("text-sm text-gray-500")

                        with ui.scroll_area().classes("w-full h-[calc(100vh-300px)]"):
                            with ui.list().props("bordered dense").classes("w-full"):
                                for trans in transactions[:100]:
                                    is_income = trans.target_account_id in account_ids
                                    amount = trans.amount_numeric if is_income else -trans.amount_numeric
                                    row_class = "bg-blue-50/50" if is_income else ""

                                    with ui.item().classes(f"px-3 py-2 {row_class}"):
                                        with ui.item_section():
                                            ui.icon("arrow_upward" if is_income else "arrow_downward") \
                                                .classes("text-green-600" if is_income else "text-red-600")
                                        with ui.item_section().classes("min-w-0"):
                                            ui.label(trans.description).classes("text-sm font-medium truncate")
                                            ui.label(trans.timestamp.strftime("%Y-%m-%d %H:%M")) \
                                                .classes("text-xs text-gray-500")
                                        with ui.item_section().props("side").classes("text-right"):
                                            ui.label(f"{amount:+.2f} {default_currency}") \
                                                .classes("text-sm font-medium " + (
                                                "text-green-600" if is_income else "text-red-600"))

                render_transactions()

        with ui.column().classes("w-full mt-4 bg-white p-4 rounded-lg border"):
            with ui.row().classes("items-center justify-between w-full mb-3"):
                ui.label("Podsumowanie finansowe").classes("text-lg font-semibold text-gray-700")

            summary_chart_ref['chart'] = ui.echart(options={
                "xAxis": {"type": "category", "data": []},
                "yAxis": {"type": "value"},
                "series": []
            }).classes("w-full h-64")

            with ui.row().classes("w-full justify-around mt-4"):
                with ui.column().classes("items-center"):
                    ui.label("Wpływy").classes("text-sm text-gray-600")
                    income_label_ref['label'] = ui.label("+0.00").classes("text-lg font-bold text-green-600")

                with ui.column().classes("items-center"):
                    ui.label("Wydatki").classes("text-sm text-gray-600")
                    expense_label_ref['label'] = ui.label("-0.00").classes("text-lg font-bold text-red-600")

                with ui.column().classes("items-center"):
                    ui.label("Bilans").classes("text-sm text-gray-600")
                    balance_label_ref['label'] = ui.label("+0.00").classes("text-lg font-bold text-green-600")

    ui.timer(0.1, update_summary_chart)
