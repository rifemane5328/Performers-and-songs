from sqlmodel import SQLModel, Field
from typing import Optional


class PerformerFilter(SQLModel):
    pseudonym: Optional[str] = Field(default=None, max_length=64)
    performance_type: Optional[str] = Field(default=None, max_length=20)
