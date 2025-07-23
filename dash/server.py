
from dash.routes import router as BaseRouter
from contextlib import asynccontextmanager
from dash import state, logging
from fastapi import FastAPI

import warnings
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
        handlers=[logging.Console],
        level=logging.INFO
    )

    config_path = os.environ.get('DASH_CONFIG', 'config.py')
    state.initialize(config_path)
    yield
    state.on_shutdown()

api = FastAPI(
    title='Dash',
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)
api.include_router(BaseRouter)
