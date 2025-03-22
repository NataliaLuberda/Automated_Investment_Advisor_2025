from nicegui import ui


@ui.page("/home")
def home_page():
    ui.label("🏠 Strona Główna").classes("text-h4")
    ui.button("Wyloguj", on_click=lambda: ui.navigate.to("/login"))
