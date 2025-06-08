from nicegui import ui
from application.models import Transakcja
from application.utils.user_info import UserInfo
from application.cqrs.commands.wyslij_przelew import WyslijPrzelew


def przelew_form(user_info: "UserInfo") -> None:
    transakcja = Transakcja()

    with ui.row().classes("flex justify-center items-center"):
        nowy_przelew_button = ui.button(
            "Nowy przelew",
            icon="add",
            on_click=lambda: setattr(nowy_przelew_button, "visible", False),
        )

    with ui.column().bind_visibility_from(
        nowy_przelew_button, "visible", lambda x: not x
    ).classes("w-full border-4"):
        select_options = {acc.id: f"{acc.currency}" for acc in user_info.account_list}

        ui.select(
            options=select_options, label="Z rachunku:", value=transakcja.id_sender
        ).classes("w-full").bind_value(transakcja, "id_sender")

        ui.number(
            label="Kwota przelewu", value=0, min=0.01, max=999999999.99, step=1.0
        ).classes("flex w-full justify-center items-center").bind_value(
            transakcja, "amount_numeric"
        )

        ui.number(label="Numer rachunku adresata").bind_value(
            transakcja, "id_receiver"
        ).classes("w-full")

        ui.textarea(
            label="Opis przelewu",
            validation={
                "Zbyt długi opis": lambda x: len(x or "") <= transakcja.MAX_DESC_LENGTH
            },
        ).classes("w-full").bind_value(transakcja, "description").props(
            f"maxlength={transakcja.MAX_DESC_LENGTH}"
        )

        with ui.row().classes("w-full flex justify-between"):

            ui.button(
                "Wyślij",
                icon="send",
                on_click=lambda: _wyslij_przelew_onclick(
                    nowy_przelew_button, transakcja
                ),
            )

            ui.button("Anuluj", icon="cancel").props("color=red")


async def _wyslij_przelew_onclick(
    element_to_toggle_visible, transakcja: Transakcja
) -> None:
    request = WyslijPrzelew.Request(
        id_nadawcy=transakcja.id_sender,
        id_adresata=transakcja.id_receiver,
        kwota=transakcja.amount_numeric,
        opis=transakcja.description,
    )
    try:
        await WyslijPrzelew.handle(request)
        ui.notify(f"Wysłano przelew! 🚀", type="positive")
        setattr(element_to_toggle_visible, "visible", True)

    except Exception as e:
        ui.notify(f"Wysyłka nie powiodła się: {e}", type="negative")
