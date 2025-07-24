
from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Any, Iterable
from dash.data import Postgres
from requests import Session
from types import ModuleType
from importlib import util
from dash import logging
from redis import Redis

state_database: Postgres | None = None
state_config: ModuleType | None = None
state_requests: Session | None = None
state_redis: Redis | None = None

def requests() -> Session:
    assert state_requests is not None, "Requests session not initialized"
    return state_requests

def redis() -> Redis | None:
    assert state_redis is not None, "Redis not initialized"
    return state_redis

def database() -> Postgres | None:
    assert state_database is not None, "Database not initialized"
    return state_database

def database_session() -> Iterable[Session]:
    assert state_database is not None, "Database not initialized"
    with state_database.session() as session:
        yield session

def config() -> ModuleType:
    assert state_config is not None, "Config not initialized"
    return state_config

def config_value(key: str, default: Any = None) -> Any:
    assert state_config is not None, "Config not initialized"
    return getattr(state_config, key, default)

def config_set_value(key: str, value: Any) -> None:
    assert state_config is not None, "Config not initialized"
    setattr(state_config, key, value)

def initialize(config_file: str) -> None:
    global state_database, state_config, state_redis, state_requests
    
    was_initialized = any([state_database, state_config, state_redis, state_requests])
    assert not was_initialized, "State already initialized"

    config_spec = util.spec_from_file_location("config", config_file)
    assert config_spec is not None, f"Config file {config_file} not found"

    config_module = util.module_from_spec(config_spec)
    config_spec.loader.exec_module(config_module)
    state_config = config_module

    state_database = Postgres(
        state_config.POSTGRES_USER,
        state_config.POSTGRES_NAME,
        state_config.POSTGRES_PASSWORD,
        state_config.POSTGRES_HOST,
        state_config.POSTGRES_PORT
    )
    state_redis = Redis(
        host=state_config.REDIS_ADDRESS,
        port=state_config.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    state_requests = Session()
    state_requests.headers.update({
        "User-Agent": f"Dash/{state_config.SITE_NAME}"
    })

def on_shutdown() -> None:
    global state_database, state_config, state_redis, state_requests

    if state_redis:
        state_redis.close()

    if state_requests:
        state_requests.close()

def setup_logging() -> None:
    logging.basicConfig(
        format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
        handlers=[logging.Console],
        level=logging.INFO
    )
