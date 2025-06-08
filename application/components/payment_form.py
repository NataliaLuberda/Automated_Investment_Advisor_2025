from nicegui import ui
from application.models import Transaction
from application.utils.user_info import UserInfo
from application.cqrs.commands.transfer_funds import TransferFunds
from application.utils.user_info import UserInfo


class PaymentForm:
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

        transaction = Transaction()

        with ui.element().classes("w-full bg-white p-4 rounded-xl") as form:

            with ui.column().classes("w-full"):
                select_options = {
                    acc.id: f"{acc.currency} (Nr. Rachunku: {acc.id})"
                    for acc in user_info.account_list
                }
                ui.select(
                    options=select_options,
                    label="Z rachunku:",
                    value=transaction.source_account_id,
                ).classes("w-full").bind_value(transaction, "source_account_id")

                ui.number(
                    label="Kwota przelewu",
                    value=0,
                    min=0.01,
                    max=999999999.99,
                    step=1.0,
                ).classes("flex w-full justify-center items-center").bind_value(
                    transaction, "amount_numeric"
                )

                ui.number(label="Numer rachunku adresata").bind_value(
                    transaction, "target_account_id"
                ).classes("w-full")

                ui.textarea(
                    label="Opis przelewu",
                    validation={
                        "Zbyt długi opis": lambda x: len(x or "")
                        <= transaction.MAX_DESC_LENGTH
                    },
                ).classes("w-full").bind_value(transaction, "description").props(
                    f"maxlength={transaction.MAX_DESC_LENGTH}"
                )

                with ui.row().classes("w-full flex justify-between"):

                    ui.button(
                        "Wyślij",
                        icon="send",
                        on_click=lambda: (self.send_transfer_onclick(transaction)),
                    )

                    ui.button(
                        "Anuluj",
                        icon="cancel",
                        on_click=lambda x: (self.hide_form_show_button()),
                    ).props("color=red")

        return form

    async def send_transfer_onclick(self, transaction: Transaction) -> None:

        request = TransferFunds.Request(transaction=transaction)
        try:
            await TransferFunds.handle(request)
            ui.notify(f"Wysłano przelew! 🚀", type="positive")
            self.hide_form_show_button()

        except Exception as e:
            ui.notify(f"Płatność nie powiodła się: {e}", type="negative")
