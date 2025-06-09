from nicegui import ui
from application.session import logout_user


def navbar() -> None:

    with ui.row().classes(
        "w-full justify-between items-center px-10 py-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg rounded-lg"
    ) as navbar:
        ui.button(icon="savings", on_click=lambda: ui.navigate.to("/savings")).props(
            "flat color=white"
        )
        ui.button(icon="bar_chart", on_click=lambda: ui.navigate.to("/transaction")).props(
            "flat color=white"
        ).tooltip("Historia transakcji")
        ui.button(
            icon="account_balance", on_click=lambda: ui.navigate.to("/account")
        ).props("flat color=white").tooltip("Szczegóły kont")
        ui.button(icon="send", on_click=lambda: (ui.navigate.to("/payments"))).props(
            "flat color=white"
        ).tooltip("Wyślij przelew")
        ui.button(
            icon="logout",
            on_click=lambda: (logout_user(), ui.navigate.to("/login")),
        ).props("flat color=white")
