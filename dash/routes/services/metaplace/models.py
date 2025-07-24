
from pydantic import BaseModel

class SNFResponse(BaseModel):
    hasError: bool = False
    error: str = ""
    data: str = ""
