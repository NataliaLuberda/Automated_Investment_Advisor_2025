from nicegui import ui

from application.auth import is_user_data_correct
from application.session import set_logged_user


def input_style():
    return "w-full mb-4 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"


def create_login_form():
    ui.label("🔐 Logowanie").classes("text-2xl font-bold mb-6 text-center text-gray-800")
    email = ui.input("Email").props("type=email").classes(input_style())
    password = ui.input("Hasło").props("type=password").classes(input_style() + " mb-2")
    return email, password


def create_login_button(email, password):
    def handle_login():
        if is_user_data_correct(email.value, password.value):
            set_logged_user(email.value)
            ui.notify(f"✅ Witaj, {email.value}!", type="positive")
            ui.navigate.to("/home")
        else:
            ui.notify("❌ Niepoprawne dane logowania", type="negative")

    ui.button("🔑 Zaloguj", on_click=handle_login).classes(
        "w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
    )


def create_register_redirect():
    with ui.row().classes("w-full mt-4 justify-center"):
        ui.label("Nie masz konta?").classes("text-gray-600")
        ui.link("Zarejestruj się", "/register").classes(
            "text-blue-500 hover:text-blue-600 transition duration-200"
        )


@ui.page('/login')
def login_page():
    with ui.row().classes("h-screen w-screen flex items-center justify-center bg-gray-100"):
        with ui.card().classes("w-96 p-8 shadow-lg rounded-lg bg-white"):
            email, password = create_login_form()
            create_login_button(email, password)
            create_register_redirect()
