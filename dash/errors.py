
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from .server import api

@api.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        {'error': exc.status_code, 'message': exc.detail},
        status_code=exc.status_code
    )

@api.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        {'error': exc.status_code, 'message': exc.detail},
        status_code=exc.status_code
    )

@api.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        {'error': 400, 'message': 'Bad Request', 'details': exc.errors()},
        status_code=400
    )

@api.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    if api.debug:
        raise exc

    return JSONResponse(
        {'error': 500, 'message': 'Internal Server Error'},
        status_code=500
    )
