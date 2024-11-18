import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, date
from fastapi import HTTPException
from services.sales_service import SalesService
from transfer.dto.sales_dto import SalesDTO, CreatedSalesDTO


class TestSalesService(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.repository_mock = MagicMock()

        with patch("services.sales_service.DatabaseConnector") as db_connector_mock, \
                patch("services.sales_service.SalesRepository") as sales_repository_mock:
            db_connector_mock.return_value.session = self.session_mock
            sales_repository_mock.return_value = self.repository_mock
            self.service = SalesService()

    def test_parse_xml_success(self):
        xml_content = b"""
        <sales_data date="2024-01-01">
            <products>
                <product>
                    <name>Item1</name>
                    <quantity>10</quantity>
                    <price>100</price>
                    <category>Category1</category>
                </product>
            </products>
        </sales_data>
        """
        result = self.service.parse_xml(xml_content)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], SalesDTO)
        self.assertEqual(result[0].good_name, "Item1")
        self.assertEqual(result[0].amount, 10)
        self.assertEqual(result[0].price, "100")
        self.assertEqual(result[0].category, "Category1")
        self.assertEqual(result[0].sales_date, datetime.strptime("2024-01-01", "%Y-%m-%d").date())

    def test_parse_xml_invalid_root_element(self):
        xml_content = b"""
        <invalid_data date="2024-01-01">
            <products>
                <product>
                    <name>Item1</name>
                    <quantity>10</quantity>
                    <price>100</price>
                    <category>Category1</category>
                </product>
            </products>
        </invalid_data>
        """
        with self.assertRaises(HTTPException) as context:
            self.service.parse_xml(xml_content)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Invalid XML format", context.exception.detail)

    def test_parse_xml_missing_fields(self):
        xml_content = b"""
        <sales_data date="2024-01-01">
            <products>
                <product>
                    <quantity>10</quantity>
                    <price>100</price>
                </product>
            </products>
        </sales_data>
        """
        with self.assertRaises(HTTPException) as context:
            self.service.parse_xml(xml_content)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Invalid product data", context.exception.detail)

    def test_parse_xml_malformed(self):
        xml_content = b"<sales_data><products><product><name>Item1"
        with self.assertRaises(HTTPException) as context:
            self.service.parse_xml(xml_content)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Malformed XML file", context.exception.detail)

    def test_batch_create(self):
        sales_dto = [SalesDTO("Item1", 10, "100", datetime.today().date(), "Category1")]
        created_sales = [CreatedSalesDTO(1, "Item1", 10, "100", datetime.today().date())]
        self.repository_mock.batch_create.return_value = created_sales
        result = self.service.batch_create(sales_dto)
        self.repository_mock.batch_create.assert_called_once_with(sales_dto)
        self.assertEqual(result, created_sales)

    def test_get_top_goods_by_date(self):
        sale_date = date(2024, 1, 1)
        self.repository_mock.get_top_goods_by_date.return_value = [("Item1", "Category1"), ("Item2", "Category2")]

        result = self.service.get_top_goods_by_date(sale_date, limit=2)
        self.repository_mock.get_top_goods_by_date.assert_called_once_with(sale_date, 2)
        self.assertEqual(result, [
            {"good_name": "Item1", "category": "Category1"},
            {"good_name": "Item2", "category": "Category2"}
        ])

    def test_get_total_revenue_by_date(self):
        sale_date = date(2024, 1, 1)
        self.repository_mock.get_total_revenue_by_date.return_value = 500.0

        result = self.service.get_total_revenue_by_date(sale_date)
        self.repository_mock.get_total_revenue_by_date.assert_called_once_with(sale_date)
        self.assertEqual(result, 500.0)


if __name__ == "__main__":
    unittest.main()
