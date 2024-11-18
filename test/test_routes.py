import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

from presentations.routes.sales import router


class TestCreatePromptFromFile(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        app.include_router(router)

    @patch("sales.SalesService")
    @patch("sales.generate_prompt")
    def test_create_prompt_success(self, mock_generate_prompt, mock_sales_service):
        mock_sales_service_instance = MagicMock()
        mock_sales_service.return_value = mock_sales_service_instance
        mock_sales_service_instance.parse_xml.return_value = \
            [
                {"id": 1,
                 "good_name": "Item",
                 "amount": 10,
                 "price": 100,
                 "sales_date": "2024-01-01"
                 }
            ]
        mock_sales_service_instance.batch_create.return_value = \
            [
                MagicMock
                (
                    id=1,
                    good_name="Item",
                    amount=10,
                    price=100, sales_date="2024-01-01"
                )
            ]
        mock_generate_prompt.delay = MagicMock()

        test_file = ("test.xml",
                     "<sales><item><id>1</id><good_name>Item</good_name><amount>10</amount>"
                     "<price>100</price><sales_date>2024-01-01</sales_date></item></sales>",
                     "application/xml"
                     )

        response = self.client.post("/create_prompt/", files={"file": test_file})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            [
                {"id": 1,
                 "good_name": "Item",
                 "amount": 10,
                 "price": 100,
                 "sales_date": "2024-01-01"
                 }
            ]
                             )

        mock_sales_service_instance.parse_xml.assert_called_once()
        mock_sales_service_instance.batch_create.assert_called_once()
        mock_generate_prompt.delay.assert_called_once_with("2024-01-01")

    def test_create_prompt_invalid_file_format(self):
        test_file = ("test.txt", "Some content", "text/plain")

        response = self.client.post("/create_prompt/", files={"file": test_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid file format")

    @patch("your_module_name.SalesService")
    def test_create_prompt_service_error(self, mock_sales_service):
        mock_sales_service_instance = MagicMock()
        mock_sales_service.return_value = mock_sales_service_instance
        mock_sales_service_instance.parse_xml.side_effect = Exception("Parsing error")

        test_file = (
                     "test.xml",
                     "<sales><item></item></sales>",
                     "application/xml"
                     )

        response = self.client.post("/create_prompt/",
                                    files={
                                        "file": test_file
                                           }
                                    )

        self.assertEqual(response.status_code, 500)
