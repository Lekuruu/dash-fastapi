
from fastapi import APIRouter
from . import autocomplete

router = APIRouter()
router.include_router(autocomplete.router)
