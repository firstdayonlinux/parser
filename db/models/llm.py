from typing import Optional

from sqlalchemy.orm import Mapped
from db.models.base import BaseModel


class Llm(BaseModel):
    __tablename__ = "llm"

    content: Mapped[str]
    llm_response: Mapped[Optional[str]]