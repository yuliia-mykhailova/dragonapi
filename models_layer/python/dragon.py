from datetime import date
from pydantic import BaseModel, constr, conint, Field


class Dragon(BaseModel):
    name: constr(max_length=250)
    breed: str
    danger_rating: conint(ge=0, le=10)
    description: str
    created_at: date = str(date.today())
