from pydantic import BaseModel


class ChatUpdate(BaseModel):
    content: dict
    type = "ChatUpdate"


class Text(BaseModel):
    content: str
    finished: bool
    type = "Text"
