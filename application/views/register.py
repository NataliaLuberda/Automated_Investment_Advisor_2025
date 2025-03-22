from nicegui import ui
from application.auth import create_user


@ui.page("/register")
def register_page():
    with ui.row().classes("h-screen w-screen flex items-center justify-center bg-gray-100"):
        with ui.card().classes("w-96 p-8 shadow-lg rounded-lg bg-white"):
            ui.label("📝 Rejestracja").classes("text-2xl font-bold mb-6 text-center text-gray-800")

            email = ui.input("Email").props("type=email").classes(
                "w-full mb-4 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            )
            password = ui.input("Hasło").props("type=password").classes(
                "w-full mb-4 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            )
            password_confirm = ui.input("Potwierdź hasło").props("type=password").classes(
                "w-full mb-6 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            )

            def handle_register():
                if password.value != password_confirm.value:
                    ui.notify("❌ Hasła nie są identyczne", type="negative")
                    return

                if create_user(email.value, password.value):
                    ui.notify("✅ Rejestracja powiodła się!", type="positive")
                    ui.open("/login")
                else:
                    ui.notify("❌ Użytkownik o takim email już istnieje", type="negative")

            ui.button("📝 Zarejestruj się", on_click=handle_register).classes(
                "w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition duration-200"
            )

            with ui.row().classes("w-full mt-4 justify-center"):
                ui.label("Masz już konto?").classes("text-gray-600")
                ui.link("Zaloguj się", "/login").classes("text-blue-500 hover:text-blue-600 transition duration-200")
