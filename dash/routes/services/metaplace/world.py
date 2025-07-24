
from .responses import error_response, world_response
from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import PlainTextResponse
from types import ModuleType
from redis import Redis
from dash import state

allowed_products = ["cjsnow"]
router = APIRouter()

@router.get("/swrequest")
def start_world_request(
    request: Request,
    token: str = Query(...),
    owner: int = Query(...),
    product_name: str = Query(...),
    world_name: str = Query(..., alias="name"),
    redis: Redis = Depends(state.redis),
    config: ModuleType = Depends(state.config)
) -> PlainTextResponse:
    if product_name not in allowed_products:
        return error_response(3514, 'Product type not supported')

    session_key = redis.get(f'{owner}.mpsession')
    
    if not session_key:
        return error_response(4408, 'Token timeout')
    
    if session_key.decode() != token:
        return error_response(3525, 'Invalid token')
    
    return world_response(token, world_name, config.CJS_HOST, config.CJS_PORT)
