from datetime import date

from sqlalchemy import NUMERIC
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel


class Sales(BaseModel):
    __tablename__ = "sales"
    good_name: Mapped[str]
    amount: Mapped[int]
    price: Mapped[int] = mapped_column(NUMERIC, nullable=False)
    sales_date: Mapped[date]
    category: Mapped[str]