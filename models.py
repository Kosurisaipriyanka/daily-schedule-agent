from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    name: str
    duration: float = Field(gt=0)
    priority: int = Field(ge=1, le=3)

    fixed_start: Optional[str] = None
    fixed_end: Optional[str] = None