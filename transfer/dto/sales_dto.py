from dataclasses import dataclass
from datetime import date
from uuid import UUID

from transfer.dto.base import BaseDTO


@dataclass(frozen=True)
class SalesDTO(BaseDTO):
    good_name: str
    amount: int
    price: str
    sales_date: date
    category: str

@dataclass(frozen=True)
class CreatedSalesDTO(SalesDTO):
    id: UUID

