from datetime import date
from uuid import UUID

from pydantic import BaseModel


class SalesResponse(BaseModel):
    id: UUID
    good_name: str
    amount: int
    price: int
    sales_date: date