
from dash.data.repositories.wrapper import session_wrapper
from dash.data.database.schemas import Penguin
from sqlalchemy.orm import Session

@session_wrapper
def fetch_by_id(penguin_id: int, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.id == penguin_id) \
        .first()

@session_wrapper
def fetch_by_name(name: str, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.username == name) \
        .first()

@session_wrapper
def fetch_by_nickname(nickname: str, session: Session = ...) -> Penguin | None:
    return session.query(Penguin) \
        .filter(Penguin.nickname == nickname) \
        .first()

@session_wrapper
def update(penguin_id: int, updates: dict, session: Session = ...) -> int:
    updated_rows = session.query(Penguin) \
        .filter(Penguin.id == penguin_id) \
        .update(updates)
    session.commit()
    return updated_rows
