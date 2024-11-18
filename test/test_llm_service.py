import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from services.llm_service import LlmService
from transfer.dto.llm_dto import LlmDTO


class TestLlmService(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.repository_mock = MagicMock()

        with patch("services.llm_service.DatabaseConnector") as db_connector_mock, \
                patch("services.llm_service.LlmRepository") as llm_repository_mock:
            db_connector_mock.return_value.session = self.session_mock
            llm_repository_mock.return_value = self.repository_mock
            self.service = LlmService()

    def test_create_filled_prompt(self):
        sale_date = date(2024, 1, 1)
        total_revenue = 1000.0
        top_products = ["Product1", "Product2", "Product3"]
        categories = ["Category1", "Category2"]

        expected_prompt = """
            Проанализируй данные о продажах за 2024-01-01:
            1. Общая выручка: 1000.0
            2. Топ-3 товара по продажам: ['Product1', 'Product2', 'Product3']
            3. Распределение по категориям: ['Category1', 'Category2']

            Составь краткий аналитический отчет с выводами и рекомендациями.
        """

        self.service.create(sale_date, total_revenue, top_products, categories)

        self.repository_mock.create.assert_called_once()
        llm_dto_argument = self.repository_mock.create.call_args[0][0]

        self.assertIsInstance(llm_dto_argument, LlmDTO)
        self.assertEqual(llm_dto_argument.content.strip(), expected_prompt.strip())
        self.assertIsNone(llm_dto_argument.llm_response)


if __name__ == "__main__":
    unittest.main()
