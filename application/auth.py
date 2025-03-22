import bcrypt
from application.database import SessionLocal
from application.models import User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()


def is_user_data_correct(email: str, password: str) -> bool:
    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if user and verify_password(password, user.password_hash):
            return True
        else:
            return False
    finally:
        db.close()


def create_user(email: str, password: str) -> bool:
    db = SessionLocal()
    try:
        if get_user_by_email(db, email):
            return False

        new_user = User(
            email=email,
            password_hash=hash_password(password)
        )
        db.add(new_user)
        db.commit()
        return True
    finally:
        db.close()
