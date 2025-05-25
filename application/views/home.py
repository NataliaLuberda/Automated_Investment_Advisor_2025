from nicegui import ui, context

from application.session import logout_user


@ui.page("/home")
def home_page():
    ui.label("🏠 Strona Główna").classes("text-h4")
    ui.button("Wyloguj", on_click=lambda: (logout_user(context.client), ui.navigate.to("/login")))
    ui.button("Konta", on_click=lambda: ui.navigate.to("/account"))
