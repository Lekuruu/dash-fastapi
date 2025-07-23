
from fastapi import HTTPException, APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from types import ModuleType

from dash.data.repositories import activations, penguins
from dash.data import Penguin, ActivationKey
from dash import state

router = APIRouter()

@router.get("/{activation_key}")
def legacy_activation(
    activation_key: str,
    config: ModuleType = Depends(state.config),
    database: Session = Depends(state.database_session),
) -> RedirectResponse:
    if not (activation_entry := activations.fetch_one(activation_key, database)):
        raise HTTPException(
            status_code=404,
            detail="Activation key not found"
        )

    was_updated = penguins.update(
        activation_entry.penguin_id,
        {'active': True},
        session=database
    )

    if not was_updated:
        raise HTTPException(
            status_code=500,
            detail="Failed to activate penguin"
        )

    activations.delete(activation_key, database)
    return RedirectResponse(config.LEGACY_ACTIVATE_REDIRECT)
