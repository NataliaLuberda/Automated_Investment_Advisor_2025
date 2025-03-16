from application.database import get_user


def is_user_data_correct(email, password):
    user = get_user(email)
    if user and user["password"] == password:
        return True
    else:
        return False
