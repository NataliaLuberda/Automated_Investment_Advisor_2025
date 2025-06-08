from nicegui import ui
from application.models import Transakcja
from application.utils.user_info import UserInfo
from application.cqrs.commands.wyslij_przelew import WyslijPrzelew
from application.utils.user_info import UserInfo


class PrzelewForm:
    def __init__(self, user_info: UserInfo) -> None:

        with ui.element().classes("w-full flex justify-center"):
            with ui.element() as self.button_container:
                self.button_reference = (
                    ui.button(
                        "Nowy przelew",
                        icon="add",
                        on_click=lambda: (self.show_form_hide_button()),
                    )
                    .props("color=white text-color=blue")
                    .classes("duration-150 hover:scale-105")
                )

            with ui.element().classes("w-full") as self.form_container:
                self.form_container.visible = False
                self.form_reference = self.przelew_form(user_info)

        return

    def show_form_hide_button(self):
        self.button_container.visible = False
        self.form_container.visible = True

    def hide_form_show_button(self):
        self.form_container.visible = False
        self.button_container.visible = True

    def przelew_form(self, user_info: "UserInfo") -> ui.element:

        transakcja = Transakcja()

        with ui.element().classes("w-full bg-white p-4 rounded-xl") as form:

            with ui.column().classes("w-full"):
                select_options = {
                    acc.id: f"{acc.currency}" for acc in user_info.account_list
                }

                ui.select(
                    options=select_options,
                    label="Z rachunku:",
                    value=transakcja.id_sender,
                ).classes("w-full").bind_value(transakcja, "id_sender")

                ui.number(
                    label="Kwota przelewu",
                    value=0,
                    min=0.01,
                    max=999999999.99,
                    step=1.0,
                ).classes("flex w-full justify-center items-center").bind_value(
                    transakcja, "amount_numeric"
                )

                ui.number(label="Numer rachunku adresata").bind_value(
                    transakcja, "id_receiver"
                ).classes("w-full")

                ui.textarea(
                    label="Opis przelewu",
                    validation={
                        "Zbyt długi opis": lambda x: len(x or "")
                        <= transakcja.MAX_DESC_LENGTH
                    },
                ).classes("w-full").bind_value(transakcja, "description").props(
                    f"maxlength={transakcja.MAX_DESC_LENGTH}"
                )

                with ui.row().classes("w-full flex justify-between"):

                    ui.button(
                        "Wyślij",
                        icon="send",
                        on_click=lambda: (self.wyslij_przelew_onclick(transakcja)),
                    )

                    ui.button(
                        "Anuluj",
                        icon="cancel",
                        on_click=lambda x: (self.hide_form_show_button()),
                    ).props("color=red")

        return form

    async def wyslij_przelew_onclick(self, transakcja: Transakcja) -> None:
        request = WyslijPrzelew.Request(
            id_nadawcy=transakcja.id_sender,
            id_adresata=transakcja.id_receiver,
            kwota=transakcja.amount_numeric,
            opis=transakcja.description,
        )
        try:
            await WyslijPrzelew.handle(request)
            ui.notify(f"Wysłano przelew! 🚀", type="positive")
            self.hide_form_show_button()

        except Exception as e:
            ui.notify(f"Płatność nie powiodła się: {e}", type="negative")
