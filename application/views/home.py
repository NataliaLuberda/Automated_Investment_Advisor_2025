from nicegui import ui

from application.session import logout_user


@ui.page("/home")
def home_page():
    ui.label("🏠 Strona Główna").classes("text-h4")
    ui.button("Wyloguj", on_click=lambda: (logout_user(), ui.navigate.to("/login")))
    ui.button("Konta", on_click=lambda: ui.navigate.to("/account"))
