from datetime import datetime

from pydantic import BaseModel


class STaskAdd(BaseModel):
    id: int
    title: str
    description: str | None
    create_at: datetime
    update_at: datetime | None
