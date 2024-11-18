from datetime import date
from typing import Optional

from sqlalchemy import func, desc

from db.models.sales import Sales
from db.repositories.base import SQLAlchemyRepository
from transfer.dto.sales_dto import SalesDTO, CreatedSalesDTO


class SalesRepository(SQLAlchemyRepository[Sales]):
    model = Sales

    def batch_create(self, sales: list[SalesDTO]) -> list[Optional[CreatedSalesDTO]]:
        result: list[Optional[CreatedSalesDTO]] = []
        for sale in sales:
            result.append(self.create(sale))
        return result

    def create(self, sale: SalesDTO) -> CreatedSalesDTO:
        with self._session() as session:
            sale_model = self.model(
                good_name=sale.good_name,
                amount=sale.amount,
                price=sale.price,
                sales_date=sale.sales_date,
                category=sale.category,
            )
            session.add(sale_model)
            session.flush()
            session.refresh(sale_model)
            return CreatedSalesDTO(
                id=sale_model.id,
                good_name=sale.good_name,
                amount=sale.amount,
                price=sale.price,
                sales_date=sale.sales_date,
                category=sale.category,
            )

    def get_top_goods_by_date(self, sale_date: date, limit: int = 3):
        with self._session() as session:
            query = (
                session.query(
                    self.model.good_name,
                    self.model.category,
                    func.sum(self.model.amount * self.model.price).label("total_revenue")
                )
                .filter(
                        self.model.sales_date == sale_date,
                )
                .group_by(self.model.good_name)
                .order_by(desc("total_revenue"))
                .limit(limit)
            )
            return query.all()

    def get_total_revenue_by_date(self, sale_date: date):
        with self._session() as session:
            total_revenue_query = (
                session.query(func.sum(self.model.amount * self.model.price).label("total_revenue"))
                .filter(
                    self.model.sales_date == sale_date,
                )
            )
            return total_revenue_query.scalar()
