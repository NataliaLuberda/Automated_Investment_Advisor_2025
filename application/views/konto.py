from nicegui import ui


@ui.page('/')
def konto_page():
    ui.add_head_html('''
        <style>
            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
        </style>
        ''')
    with ui.element('div').classes('w-screen h-screen flex items-center justify-center'):
        with ui.card().classes('flex flex-col items-center justify-center'):
            ui.label("hello")
            with ui.card_section():
                ui.label("something else")