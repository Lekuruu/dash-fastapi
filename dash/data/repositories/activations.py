
from dash.data.repositories.wrapper import session_wrapper
from dash.data.database.schemas import ActivationKey
from sqlalchemy.orm import Session

@session_wrapper
def create(
    penguin_id: int,
    activation_key: str,
    session: Session = ...
) -> ActivationKey:
    activation = ActivationKey(
        penguin_id=penguin_id,
        activation_key=activation_key
    )
    session.add(activation)
    session.commit()
    session.refresh(activation)
    return activation

@session_wrapper
def fetch_one(
    activation_key: str,
    session: Session = ...
) -> ActivationKey | None:
    return session.query(ActivationKey) \
        .filter(ActivationKey.activation_key == activation_key) \
        .first()

@session_wrapper
def delete(
    penguin_id: int,
    session: Session = ...
) -> bool:
    deleted_rows = session.query(ActivationKey) \
        .filter(ActivationKey.penguin_id == penguin_id) \
        .delete()
    session.commit()
    return deleted_rows > 0
