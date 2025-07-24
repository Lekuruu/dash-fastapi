
from fastapi import APIRouter
from . import avatar

router = APIRouter()
router.include_router(avatar.router)
