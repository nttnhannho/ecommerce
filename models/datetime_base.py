from datetime import datetime

from pydantic import BaseModel, Field


class DatetimeBase(BaseModel):
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = Field(default=None)
    deleted_at: datetime = Field(default=None)
