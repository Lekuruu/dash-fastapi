
from fastapi import APIRouter

from . import vanilla
from . import legacy

router = APIRouter()
router.include_router(vanilla.router, prefix="/vanilla")
router.include_router(legacy.router, prefix="/legacy")
