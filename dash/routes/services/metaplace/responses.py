
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

class SNFResponse(BaseModel):
    hasError: bool = False
    error: str = ""
    data: str = ""

def world_response(
    token: str,
    world_name: str,
    host: str,
    port: int,
    owner: str = 'crowdcontrol',
    branch: str = 'CPNext_dev_branch'
) -> PlainTextResponse:
    return PlainTextResponse(
        f'[S_WORLDLIST]|{token}|{world_name}|{host}|{port}||{owner}|{world_name}|{branch}|example'
    )

def error_response(
    code: int = 1,
    message: str = "Internal Error",
    title: str = "Cannot Start World"
) -> PlainTextResponse:
    return PlainTextResponse(
        f'[S_ERROR]|{code}|{title}|{message}'
    )
