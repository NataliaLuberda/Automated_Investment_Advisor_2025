from nicegui import ui
from sqlalchemy.orm import Session
from application.services.database import get_session  
from application.models import User, Account, Transaction
from datetime import datetime, timedelta

@ui.page("/transaction")
def transaction_page():
    ui.label("🏠 Transaction_page").classes("text-h4")
    ui.button("Wyloguj", on_click=lambda: ui.navigate.to("/login"))

    user_id = ui.storage.user.get("user_id")
    if not user_id:
        ui.notify("Nie jesteś zalogowany!")
        ui.navigate.to("/login")
        return

    # -------- Pobranie danych z bazy --------
    session: Session = get_session()

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        ui.notify("Nie znaleziono użytkownika")
        return

    account_ids = [account.id for account in user.accounts]
    transactions = (
        session.query(Transaction)
        .filter(
            (Transaction.source_account_id.in_(account_ids)) |
            (Transaction.target_account_id.in_(account_ids))
        )
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    # -------- Sekcja salda --------
    main_balance = sum(account.balance for account in user.accounts)
    savings = 0 

    ui.label(f"Witaj, {user.email}!").classes("text-2xl font-bold mt-4")

    with ui.row().classes("w-full max-w-4xl justify-between"):
        with ui.card().classes("w-full max-w-sm bg-blue-50"):
            ui.label("Saldo główne").classes("text-lg text-gray-600")
            ui.label(f"{main_balance:.2f} {user.default_currency or 'PLN'}").classes("text-3xl font-bold text-green-600")

        with ui.card().classes("w-full max-w-sm bg-yellow-50"):
            ui.label("Oszczędności").classes("text-lg text-gray-600")
            ui.label(f"{savings:.2f} {user.default_currency or 'PLN'}").classes("text-3xl font-bold text-orange-500")

    ui.label("Historia transakcji").classes("text-lg font-semibold mt-6")

    with ui.list().props('bordered separator'):
        ui.item_label('Transakcje').props('header').classes('text-bold')
        ui.separator()
        for trans in transactions:
            is_income = trans.target_account_id in account_ids
            amount = trans.amount_numeric if is_income else -trans.amount_numeric
            kolor = 'text-green-600' if amount >= 0 else 'text-red-600'

            with ui.item():
                with ui.item_section().props('avatar'):
                    ui.icon('attach_money')
                with ui.item_section():
                    ui.item_label(trans.description)
                    ui.item_label(trans.timestamp.strftime('%Y-%m-%d %H:%M')).props('caption')
                with ui.item_section().props('side'):
                    ui.item_label(f"{amount:.2f}").classes(f"font-semibold {kolor}")
                with ui.item_section().props('side'):
                    ui.item_label(user.default_currency or "PLN").classes("text-gray-500 text-sm")

    # -------- Wykres podsumowujący --------
    def calculate_summary():
        income = sum(t.amount_numeric for t in transactions if t.target_account_id in account_ids)
        expense = sum(t.amount_numeric for t in transactions if t.source_account_id in account_ids)
        return income, expense

    income, expense = calculate_summary()

    summary_chart = ui.echart({
        'tooltip': {'trigger': 'axis'},
        'xAxis': {
            'type': 'category',
            'data': ['Dochody', 'Wydatki'],
            'axisLabel': {'color': 'gray'}
        },
        'yAxis': {
            'type': 'value',
            'axisLabel': {'color': 'gray'}
        },
        'series': [
            {
                'type': 'bar',
                'data': [
                    {'value': income, 'itemStyle': {'color': '#4caf50'}},
                    {'value': expense, 'itemStyle': {'color': '#f44336'}}
                ],
                'label': {'show': True, 'position': 'top', 'color': 'black'}
            }
        ]
    })

    def update_summary_chart():
        income, expense = calculate_summary()
        summary_chart.options['series'][0]['data'] = [
            {'value': income, 'itemStyle': {'color': '#4caf50'}},
            {'value': expense, 'itemStyle': {'color': '#f44336'}}
        ]
        summary_chart.update()

    ui.button('🔄 Odśwież sumy', on_click=update_summary_chart).classes("mt-2")
