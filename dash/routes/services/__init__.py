
from fastapi import APIRouter

from . import activate

router = APIRouter()
router.include_router(activate.router, prefix="/activate")
