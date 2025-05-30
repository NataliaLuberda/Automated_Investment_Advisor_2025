from application.services.database import SessionLocal
from application.models import User
from application.utils.hashing import hash_password, verify_password


def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()


def is_user_data_correct(email: str, password: str) -> bool:
    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        return user and verify_password(password, user.password_hash)
    finally:
        db.close()


def create_user(email: str, password: str) -> bool:
    db = SessionLocal()
    try:
        if get_user_by_email(db, email):
            return False
        user = User(email=email, password_hash=hash_password(password))
        db.add(user)
        db.commit()
        return True
    finally:
        db.close()
