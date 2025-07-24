
from .responses import SNFResponse
from dash.data.repositories import penguins
from dash import state

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from secrets import token_hex
from redis import Redis

router = APIRouter()

@router.post("/session", response_class=JSONResponse)
def snfgenerator(
    request: Request,
    token: str = Form(...),
    penguin_id: int = Form(..., alias="pid"),
    database: Session = Depends(state.database_session),
    redis: Redis = Depends(state.redis)
) -> SNFResponse:
    if not (penguin := penguins.fetch_by_id(penguin_id, session=database)):
        return SNFResponse(hasError=True, error="Penguin not found")

    login_key = redis.get(f'{penguin.username}.loginkey') or b''

    if login_key.decode() != token:
        return SNFResponse(hasError=True, error="Invalid token")

    session_token = token_hex(16)
    redis.setex(f'{penguin.id}.mpsession', 60, session_token)
    return SNFResponse(data=session_token)
