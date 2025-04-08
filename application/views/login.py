from nicegui import ui
from application.auth import is_user_data_correct


def create_login_form():
    ui.label("🔐 Logowanie").classes("text-2xl font-bold mb-6 text-center text-gray-800")
    email = ui.input("Email").props("type=email").classes(
        "w-full mb-4 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    )
    password = ui.input("Hasło").props("type=password").classes(
        "w-full mb-6 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    )
    return email, password


def handle_login(email, password):
    if is_user_data_correct(email.value, password.value):
        ui.notify(f"✅ Witaj, {email.value}!", type="positive")
        ui.navigate.to("/home")
    else:
        ui.notify("❌ Niepoprawne dane logowania", type="negative")


def add_login_button(email, password):
    ui.button("🔑 Zaloguj", on_click=lambda: handle_login(email, password)).classes(
        "w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
    )


def add_register_link():
    with ui.row().classes("w-full mt-4 justify-center"):
        ui.label("Nie masz konta?").classes("text-gray-600")
        ui.link("Zarejestruj się", "/register").classes("text-blue-500 hover:text-blue-600 transition duration-200")


@ui.page('/')
@ui.page('/login')
def login_page():
    with ui.row().classes("h-screen w-screen flex items-center justify-center bg-gray-100"):
        with ui.card().classes("w-96 p-8 shadow-lg rounded-lg bg-white"):
            email, password = create_login_form()
            add_login_button(email, password)
            add_register_link()
