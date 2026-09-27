from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    name: str
    duration: float
    priority: int
    fixed_start: Optional[str] = None
    fixed_end: Optional[str] = None