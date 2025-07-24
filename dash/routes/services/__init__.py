
from fastapi import APIRouter

from . import autocomplete
from . import activate

router = APIRouter()
router.include_router(activate.router, prefix="/activate")
router.include_router(autocomplete.router, prefix="/autocomplete")
