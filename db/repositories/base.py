from typing import TypeVar, Generic, Type, Generator

from sqlalchemy.orm import Session

from db.models.base import BaseModel


T = TypeVar("T", bound=BaseModel)


class SQLAlchemyRepository(Generic[T]):
    model = Type[T]

    def __init__(self, session: Type[Generator[Session, None, None]]):
        self._session = session