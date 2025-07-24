
from dash.routes import router as BaseRouter
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dash import state

import warnings
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.environ.get('DASH_CONFIG', 'config.py')
    state.initialize(config_path)
    state.setup_logging()
    yield
    state.on_shutdown()

api = FastAPI(
    title='Dash',
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)
api.include_router(BaseRouter)
