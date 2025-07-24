
from fastapi import APIRouter

from . import autocomplete
from . import activate
from . import avatar

router = APIRouter()
router.include_router(autocomplete.router, prefix="/autocomplete")
router.include_router(activate.router, prefix="/activate")
router.include_router(avatar.router, prefix="/avatar")
