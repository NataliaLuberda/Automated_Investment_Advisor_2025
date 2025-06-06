from nicegui import ui

from application.account import create_account
from application.account import get_user_accounts, delete_account
from application.auth import get_user_by_email
from application.decorator.login_decorator import requires_login
from application.session import get_logged_user_email
from application.utils.catched_total_balance import get_cached_total_balance_for_user, reset_user_balance
from application.utils.currency import fetch_currency_codes
from application.utils.transfer import transfer_between_accounts

ui.add_head_html('<link rel="stylesheet" href="/static/style.css">')


def transfer_from_account_dialog(source_acc):
    dialog = ui.dialog()
    with dialog:
        with ui.card().classes("p-6 w-[350px] flex flex-col gap-4"):
            ui.label(f"💸 Przelej z {source_acc.currency} ({source_acc.balance:.2f})").classes("text-xl font-bold")

            currencies = fetch_currency_codes()
            all_currencies = list(currencies.keys()) if currencies else ["PLN", "USD", "EUR", "GBP", "CHF", "JPY"]
            dest_currencies = [cur for cur in all_currencies if cur != source_acc.currency]

            currency_select = ui.select(
                dest_currencies,
                label="Waluta docelowa"
            ).props("clearable use-input input-debounce=0").classes("w-full")

            amount_input = ui.input(label="Kwota").props("type=number").classes("w-full")

            def handle_transfer():
                try:
                    if not currency_select.value:
                        ui.notify("❌ Wybierz walutę docelową", type="negative")
                        return

                    if not amount_input.value or float(amount_input.value) <= 0:
                        ui.notify("❌ Podaj poprawną kwotę", type="negative")
                        return

                    amount = float(amount_input.value)
                    dest_currency = currency_select.value

                    result = transfer_between_accounts(source_acc.id, dest_currency, amount)
                    ui.notify(result)
                    dialog.close()
                    reset_user_balance(get_logged_user_email())
                    ui.navigate.reload()
                except Exception as e:
                    ui.notify(f"❌ Błąd: {e}", type="negative")

            ui.button("Przelej", on_click=handle_transfer).classes(
                "bg-green-600 text-white py-1 px-4 self-end"
            )
    return dialog


def handle_delete_account(account):
    try:
        result = delete_account(account.id)
        ui.notify(result)
        reset_user_balance(get_logged_user_email())
        ui.navigate.reload()
    except Exception as e:
        ui.notify(f"{e}", type="negative")


def add_account_dialog():
    dialog = ui.dialog()

    with dialog:
        with ui.card().classes("p-6 w-[350px] flex flex-col gap-4"):
            currencies = fetch_currency_codes()
            currency_items = [f"{code} - {name}" for code, name in currencies.items()]

            currency_select = ui.select(
                currency_items,
                label="Waluta"
            ).props("clearable use-input input-debounce=0").classes("w-full")

            new_balance = ui.input(label="Saldo", placeholder="np. 1000.00").props("type=number").classes("w-full")

            def handle_add():
                try:
                    if not currency_select.value or not new_balance.value:
                        ui.notify("⚠️ Wypełnij wszystkie pola")
                        return

                    selected_code = currency_select.value.split(" - ")[0]
                    balance = float(new_balance.value)

                    result = create_account(selected_code, balance)
                    ui.notify(result)
                    dialog.close()
                    reset_user_balance(get_logged_user_email())
                    ui.navigate.reload()

                except Exception as e:
                    ui.notify(f"❌ Błąd: {e}", type="negative")

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
    accounts = get_user_accounts()

    ui.label("🌍 Inne konta walutowe").classes("text-lg font-bold text-gray-700")
    with ui.column().classes("gap-4").style("max-height: 65vh; overflow-y: auto;"):
        if foreign_accounts:
            for acc in foreign_accounts:
                transfer_dlg = transfer_from_account_dialog(acc)

                with ui.card().classes("p-4 w-full bg-white shadow rounded-lg flex flex-row justify-between "
                                       "items-center"):
                    with ui.column():
                        ui.label(f"{acc.currency}").classes("text-lg font-semibold")
                        ui.label(f"{acc.balance:.2f} {acc.currency}").classes("text-lg")

                    with ui.row().classes("gap-2"):
                        ui.button("💸", on_click=transfer_dlg.open).classes(
                            "bg-green-500 text-white py-1 px-3 rounded"
                        )
                        ui.button("🗑", on_click=lambda a=acc: handle_delete_account(a)).classes(
                            "bg-red-500 text-white py-1 px-3 rounded"
                        )
        else:
            ui.label("Brak innych kont walutowych").classes("text-gray-500 italic")


@ui.page("/account")
@requires_login
def account_page():
    email = get_logged_user_email()
    accounts = get_user_accounts()
    user = get_user_by_email(email)
    default_currency = user.default_currency if user and user.default_currency else "PLN"
    default_account = next((acc for acc in accounts if acc.currency == default_currency), None)
    foreign_accounts = [acc for acc in accounts if acc.currency != default_currency]
    total_balance = get_cached_total_balance_for_user(email, accounts)

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
