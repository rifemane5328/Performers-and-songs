from sqlmodel import SQLModel, Field


class PaginationParams(SQLModel):
    page: int = Field(1, ge=0)
    size: int = Field(100, gt=1, lt=100000)