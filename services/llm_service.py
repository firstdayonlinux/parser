from datetime import date
from typing import Generator, Type

from db.connector import DatabaseConnector
from db.repositories.llm_repository import LlmRepository
from transfer.dto.llm_dto import LlmDTO


class LlmService:
    def __init__(self):
        self._session: Type[Generator] = DatabaseConnector().session
        self._repository = LlmRepository(self._session)

    def create(self, sale_date: date, total_revenue: float, top_products: list[str], categories: list[str]) -> None:
        prompt = """
            Проанализируй данные о продажах за {date}:
            1. Общая выручка: {total_revenue}
            2. Топ-3 товара по продажам: {top_products}
            3. Распределение по категориям: {categories}
            
            Составь краткий аналитический отчет с выводами и рекомендациями.
        """

        filled_prompt = prompt.format(
                    date=sale_date,
                    total_revenue=total_revenue,
                    top_products=top_products,
                    categories=categories,
                )

        self._repository.create(LlmDTO(content=filled_prompt, llm_response=None))