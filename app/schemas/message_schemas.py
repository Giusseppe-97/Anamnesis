from pydantic import BaseModel


class DefaultMessageSchema(BaseModel):
    message: str


class HTTPException(BaseModel):
    detail: str

