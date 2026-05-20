from datetime import datetime
from pydantic import BaseModel, Field


class DataInput(BaseModel):
    date: datetime = Field(..., example="2021-01-03T12:00:00Z")

def format_date(date: DataInput) -> str:
    return date.strftime("%B %d, %Y")