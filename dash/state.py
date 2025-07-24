
from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Any, Iterable
from functools import lru_cache
from dash.data import Postgres
from requests import Session
from types import ModuleType
from dash import logging
from redis import Redis

import importlib
import jinja2

state_jinja2: jinja2.Environment | None = None
state_database: Postgres | None = None
state_config: ModuleType | None = None
state_requests: Session | None = None
state_redis: Redis | None = None

def jinja2_environment() -> jinja2.Environment:
    assert state_jinja2 is not None, "Jinja2 environment not initialized"
    return state_jinja2

@lru_cache(maxsize=128)
def jinja2_template(name: str) -> jinja2.Template:
    assert state_jinja2 is not None, "Jinja2 environment not initialized"
    return state_jinja2.get_template(name)

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
    global state_database, state_config, state_redis, state_requests, state_jinja2

    was_initialized = any([state_database, state_config, state_redis, state_requests, state_jinja2])
    assert not was_initialized, "State already initialized"

    config_spec = importlib.util.spec_from_file_location("config", config_file)
    assert config_spec is not None, f"Config file {config_file} not found"

    config_module = importlib.util.module_from_spec(config_spec)
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
        db=0
    )

    state_requests = Session()
    state_requests.headers.update({
        "User-Agent": f"Dash/{state_config.SITE_NAME}"
    })

    state_jinja2 = jinja2.Environment(
        loader=jinja2.FileSystemLoader('dash/templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )

def on_shutdown() -> None:
    global state_redis, state_requests

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
