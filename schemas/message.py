from pydantic import BaseModel
from typing import Dict

class Message(BaseModel):
    sender: str
    receiver: str
    intent: str
    payload: Dict
