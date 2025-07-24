
from fastapi import APIRouter

from . import autocomplete
from . import metaplace
from . import activate
from . import avatar

router = APIRouter()
router.include_router(activate.router, prefix="/activate")
router.include_router(avatar.router, prefix="/avatar")
router.include_router(autocomplete.router)
router.include_router(metaplace.router)
