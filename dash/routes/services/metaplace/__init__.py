
from fastapi import APIRouter

from . import session
from . import world

router = APIRouter()
router.include_router(session.router, prefix="/session")
router.include_router(world.router, prefix="/swrequest")
