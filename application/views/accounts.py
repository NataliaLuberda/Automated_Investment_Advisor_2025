from nicegui import ui
from application.account import get_user_accounts, create_account
from application.decorator.login_decorator import requires_login

ui.add_head_html('<link rel="stylesheet" href="/static/style.css">')


def add_account_dialog():
    dialog = ui.dialog()
    with dialog:
        with ui.card().classes("p-6 w-[300px] flex flex-col gap-4"):
            new_currency = ui.input(label="Waluta", placeholder="np. CHF").props("clearable")
            new_balance = ui.input(label="Saldo", placeholder="np. 1000.00").props("type=number")

            def handle_add():
                try:
                    result = create_account(new_currency.value, float(new_balance.value))
                    ui.notify(result)
                    dialog.close()
                    ui.navigate.reload()
                except Exception:
                    ui.notify("❌ Błąd podczas dodawania", type="negative")

            ui.button("Dodaj konto", on_click=handle_add).classes(
                "bg-blue-600 text-white py-1 px-4 self-end"
            )
    return dialog


def render_total_balance(total_balance: float):
    with ui.card().classes("p-6 bg-white shadow rounded-lg flex-1"):
        ui.label("💰 Suma wszystkich środków").classes("text-lg font-bold text-gray-700")
        ui.label(f"{total_balance:.2f} PLN").classes("text-3xl text-green-600")


def render_default_account(default_account):
    with ui.card().classes("p-6 bg-white shadow rounded-lg flex-1"):
        ui.label("🏦 Konto domyślne (PLN)").classes("text-lg font-bold text-gray-700")
        ui.label(f"{default_account.balance:.2f} PLN").classes("text-3xl text-blue-600")


def render_foreign_accounts(foreign_accounts):
    ui.label("🌍 Inne konta walutowe").classes("text-lg font-bold text-gray-700")
    if foreign_accounts:
        for acc in foreign_accounts:
            with ui.card().classes("p-4 bg-white shadow rounded-lg flex-1"):
                ui.label(f"{acc.currency}").classes("text-lg font-semibold")
                ui.label(f"{acc.balance:.2f} {acc.currency}").classes("text-lg")
    else:
        ui.label("Brak innych kont walutowych").classes("text-gray-500 italic")


@ui.page("/account")
@requires_login
def account_page():
    accounts = get_user_accounts()
    default_account = next((acc for acc in accounts if acc.currency == "PLN"), None)
    foreign_accounts = [acc for acc in accounts if acc.currency != "PLN"]
    total_balance = sum(acc.balance for acc in accounts)

    add_dialog = add_account_dialog()

    with ui.element("div").classes("w-screen h-screen overflow-hidden bg-gray-100 flex"):
        with ui.column().classes("w-1/2 h-full justify-start items-stretch p-8 gap-6"):
            render_total_balance(total_balance)
            if default_account:
                render_default_account(default_account)

        with ui.column().classes("w-1/2 h-full justify-start items-stretch overflow-auto p-8 gap-6"):
            render_foreign_accounts(foreign_accounts)
            ui.button("➕ Dodaj konto", on_click=add_dialog.open).classes(
                "mt-4 bg-blue-500 text-white py-2 px-6 rounded self-start"
            )
