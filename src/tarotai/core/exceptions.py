from pydantic import BaseModel

class TarotError(BaseModel):
    message: str
    code: int
