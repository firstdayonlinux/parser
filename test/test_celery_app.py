import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from celery_app import celery_app, generate_prompt


class TestCeleryApp(unittest.TestCase):
    def test_celery_configuration(self):
        self.assertIsNotNone(celery_app.conf.broker_url)
        self.assertIsNotNone(celery_app.conf.result_backend)
        self.assertEqual(celery_app.conf.timezone, "UTC")
        self.assertTrue(celery_app.conf.task_track_started)
        self.assertFalse(celery_app.conf.worker_hijack_root_logger)

    @patch("celery_app.LlmService")
    @patch("celery_app.SalesService")
    def test_generate_prompt_task(self, mock_sales_service_class, mock_llm_service_class):
        mock_sales_service = MagicMock()
        mock_llm_service = MagicMock()

        mock_sales_service_class.return_value = mock_sales_service
        mock_llm_service_class.return_value = mock_llm_service

        mock_sales_service.get_total_revenue_by_date.return_value = 1000
        mock_sales_service.get_top_goods_by_date.return_value = [
            {"categories": "Electronics", "good_names": "Laptop"},
            {"categories": "Books", "good_names": "Fiction Novel"}
        ]

        llm_date = date(2024, 11, 18)
        generate_prompt(llm_date)

        mock_sales_service.get_total_revenue_by_date.assert_called_once_with(llm_date)
        mock_sales_service.get_top_goods_by_date.assert_called_once_with(llm_date)

        mock_llm_service.create.assert_called_once_with(
            llm_date,
            1000,
            ["Laptop", "Fiction Novel"],
            ["Electronics", "Books"]
        )

    @patch("celery_app.LlmService")
    @patch("celery_app.SalesService")
    def test_generate_prompt_with_empty_top_goods(self, mock_sales_service_class, mock_llm_service_class):
        mock_sales_service = MagicMock()
        mock_llm_service = MagicMock()

        mock_sales_service_class.return_value = mock_sales_service
        mock_llm_service_class.return_value = mock_llm_service

        mock_sales_service.get_total_revenue_by_date.return_value = 500
        mock_sales_service.get_top_goods_by_date.return_value = []

        llm_date = date(2024, 11, 18)
        generate_prompt(llm_date)

        mock_llm_service.create.assert_called_once_with(
            llm_date,
            500,
            [],
            []
        )


if __name__ == "__main__":
    unittest.main()