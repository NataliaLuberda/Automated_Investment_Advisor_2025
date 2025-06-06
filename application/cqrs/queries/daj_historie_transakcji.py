from sqlalchemy import or_

from application.models import Transakcja
from application.services.database import get_db_session


def daj_historie_transakcji_uzytkownika(user_id: int) -> list[Transakcja]:
    with get_db_session() as session:
        transakcje = session.query(Transakcja) \
            .filter(or_(Transakcja.id_sender == user_id, Transakcja.id_receiver == user_id)) \
            .all()

    return transakcje
