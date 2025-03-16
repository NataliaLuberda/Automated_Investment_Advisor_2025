from nicegui import ui


def home_page():
    ui.label("🏠 Strona Główna").classes("text-h4")
    ui.button("Wyloguj", on_click=lambda: ui.open("/login"))
