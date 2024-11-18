from typing import Optional

from db.models.llm import Llm
from db.repositories.base import SQLAlchemyRepository
from transfer.dto.llm_dto import CreatedLlmDTO, LlmDTO


class LlmRepository(SQLAlchemyRepository[Llm]):
    model = Llm

    def create(self, llm: LlmDTO) -> None:
        with self._session() as session:
            result: Optional[Llm] = Llm(content=llm.content)
            session.add(result)
