from application.models import User
from application.services.database import get_db_session
from dataclasses import dataclass


class DajUzytkownika:
    @dataclass
    class Request:
        email: str

    @staticmethod
    def handle(request: Request) -> 'User':
        with get_db_session() as session:
            return session.query(User).filter(User.email == request.email).first()
