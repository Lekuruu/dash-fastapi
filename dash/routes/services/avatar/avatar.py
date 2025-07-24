
from fastapi import HTTPException, APIRouter, Request, Query, Depends
from fastapi.responses import StreamingResponse
from dash.data.repositories import penguins
from sqlalchemy.orm import Session
from typing import List
from redis import Redis
from dash import state
from PIL import Image

import logging
import os
import io

avatar_item_directory = os.path.abspath("./items")
logger = logging.getLogger("dash")

valid_sizes = [60, 88, 95, 120, 300, 600]
cache_expiry = 60 * 10

async def check_avatar_item_directory() -> None:
    if os.path.exists(avatar_item_directory):
        return

    logger.warning(
        f"Avatar directory '{avatar_item_directory}' is missing! "
        f"Either download from https://icerink.solero.me/media1.clubpenguin.com/avatar/paper/ "
        f"or let wand mount the directory for you!"
    )

router = APIRouter()
router.add_event_handler("startup", check_avatar_item_directory)

@router.get("/{penguin_id}")
def avatar(
    request: Request,
    penguin_id: str,
    size: int = Query(120),
    background: bool = Query(True, alias="photo"),
    database: Session = Depends(state.database_session),
    redis: Redis = Depends(state.redis)
) -> StreamingResponse:
    if size not in valid_sizes:
        raise HTTPException(status_code=400, detail=f"Invalid size")

    cache_key = f"{penguin_id}.{size}.{background}.avatar"
    cached_image = redis.get(cache_key)

    if cached_image:
        redis.expire(cache_key, cache_expiry)
        return StreamingResponse(io.BytesIO(cached_image), media_type="image/png")

    if not os.path.exists(avatar_item_directory):
        raise HTTPException(status_code=500, detail="Avatar item directory is missing")

    if not (penguin := penguins.fetch_by_id(penguin_id, session=database)):
        raise HTTPException(status_code=404, detail="Penguin not found")

    clothing = [
        penguin.photo,
        penguin.color,
        penguin.head,
        penguin.face,
        penguin.body,
        penguin.neck,
        penguin.hand,
        penguin.feet
    ]

    if not background:
        clothing.pop(0)

    image = build_avatar(clothing, size)
    redis.setex(cache_key, cache_expiry, image.getvalue())
    return StreamingResponse(image, media_type="image/png")

def build_avatar(clothing: List[int], size: int) -> io.BytesIO:
    avatar_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    filtered_clothing = filter(None, clothing)
    
    for item in filtered_clothing:
        image_path = f'{avatar_item_directory}/{size}/{item}.png'

        if not os.path.exists(image_path):
            continue

        item_image = Image.open(image_path)
        avatar_image.paste(item_image, (0, 0), item_image)

    output = io.BytesIO()
    avatar_image.save(output, format='PNG')
    output.seek(0)
    return output
