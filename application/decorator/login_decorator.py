from functools import wraps
from nicegui import context, ui

from application.session import get_logged_user_email


def requires_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        email = get_logged_user_email()
        if not email:
            ui.navigate.to("/login")
            return
        return func(*args, **kwargs)
    return wrapper
