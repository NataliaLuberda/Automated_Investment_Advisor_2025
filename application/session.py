from nicegui import app
from application.models import Account

def set_logged_user(email: str):
    app.storage.user['user_email'] = email

def get_logged_user_email() -> str:
    return app.storage.user.get('user_email')

def logout_user():
    app.storage.user.clear()