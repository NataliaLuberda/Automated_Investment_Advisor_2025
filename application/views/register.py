from nicegui import ui
from application.auth import create_user
from application.utils.currency import fetch_currency_codes


def input_style():
    return "w-full mb-4 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"


def create_register_form():
    ui.label("📝 Rejestracja").classes("text-2xl font-bold mb-6 text-center text-gray-800")

    email = ui.input("Email").props("type=email").classes(input_style())
    password = ui.input("Hasło").props("type=password").classes(input_style())
    password_confirm = ui.input("Potwierdź hasło").props("type=password").classes(input_style())
    currencies = fetch_currency_codes()
    currency_items = [f"{code} - {name}" for code, name in currencies.items()]
    default_currency = ui.select(
        currency_items, label="Domyślna waluta konta"
    ).props("clearable use-input input-debounce=0").classes(input_style())

    return email, password, password_confirm, default_currency


def create_register_button(email, password, password_confirm, default_currency):
    def handle_register():
        if password.value != password_confirm.value:
            ui.notify("❌ Hasła nie są identyczne", type="negative")
            return

        if not default_currency.value:
            ui.notify("❌ Wybierz domyślną walutę!", type="negative")
            return

        selected_code = default_currency.value.split(" - ")[0]

        if create_user(email.value, password.value, selected_code):
            ui.notify("✅ Rejestracja powiodła się!", type="positive")
            ui.navigate.to("/login")
        else:
            ui.notify("❌ Użytkownik o takim email już istnieje", type="negative")

    ui.button("📝 Zarejestruj się", on_click=handle_register).classes(
        "w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition duration-200"
    )


def add_login_redirect():
    with ui.row().classes("w-full mt-4 justify-center"):
        ui.label("Masz już konto?").classes("text-gray-600")
        ui.link("Zaloguj się", "/login").classes(
            "text-blue-500 hover:text-blue-600 transition duration-200"
        )


@ui.page("/register")
def register_page():
    with ui.row().classes("h-screen w-screen flex items-center justify-center bg-gray-100"):
        with ui.card().classes("w-96 p-8 shadow-lg rounded-lg bg-white"):
            email, password, password_confirm = create_register_form()
            create_register_button(email, password, password_confirm)
            add_login_redirect()
