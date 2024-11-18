from datetime import datetime, date
from typing import Generator, Type

from db.connector import DatabaseConnector
from db.repositories.sales_repository import SalesRepository
import xml.etree.ElementTree as ET
from fastapi import HTTPException, status

from transfer.dto.sales_dto import SalesDTO, CreatedSalesDTO


class SalesService:
    def __init__(self):
        self._session: Type[Generator] = DatabaseConnector().session
        self._repository = SalesRepository(self._session)

    def parse_xml(self, file_content: bytes) -> list[SalesDTO]:
        try:
            root = ET.fromstring(file_content.decode("utf-8"))

            if root.tag != "sales_data":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid XML format: Root element must be 'sales_data'",
                )

            products = []
            sales_date = datetime.strptime(root.attrib.get("date"), "%Y-%m-%d").date()
            for product_elem in root.findall(".//products/product"):
                try:
                    good_name = product_elem.find("name").text
                    amount = int(product_elem.find("quantity").text)
                    price = product_elem.find("price").text
                    category = product_elem.find("category").text

                    if good_name is None or amount is None or price is None:
                        raise ValueError("Missing required product data")

                    product_dto = SalesDTO(
                        good_name=good_name,
                        amount=amount,
                        price=price,
                        sales_date=sales_date,
                        category=category,
                    )
                    products.append(product_dto)

                except (AttributeError, ValueError) as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid product data: {e}",
                    ) from e

            return products

        except ET.ParseError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Malformed XML file",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {e}",
            ) from e

    def batch_create(self, sales: list[SalesDTO]) -> list[CreatedSalesDTO]:
        return self._repository.batch_create(sales)

    def get_top_goods_by_date(self, sale_date: date, limit: int = 3) -> list[dict]:
        top_goods: list[tuple] = self._repository.get_top_goods_by_date(sale_date, limit)
        return [{'good_name': value[0], "category": value[1]} for value in top_goods]

    def get_total_revenue_by_date(self, sale_date: date) -> float:
        total_revenue = self._repository.get_total_revenue_by_date(sale_date)
        return total_revenue

