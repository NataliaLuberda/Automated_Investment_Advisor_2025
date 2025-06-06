from application.models import User, Account
from application.services.database import get_db_session
from application.utils.hashing import hash_password, verify_password


def get_user_by_email(email: str):
    with get_db_session() as db:
        return db.query(User).filter(User.email == email).first()


def is_user_data_correct(email: str, password: str) -> bool:
    user = get_user_by_email(email)
    return user and verify_password(password, user.password_hash)


def create_user(email: str, password: str, default_currency: str) -> bool:
    with get_db_session() as db:
        if get_user_by_email(email):
            return False
        user = User(
            email=email,
            password_hash=hash_password(password),
            default_currency=default_currency.upper()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        account = Account(currency=default_currency.upper(), balance=0.0, user_id=user.id)
        db.add(account)
        db.commit()
        return True
