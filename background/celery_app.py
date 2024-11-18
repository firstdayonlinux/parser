from celery import Celery
from config import settings

from datetime import date

from services.llm_service import LlmService
from services.sales_service import SalesService


redis_url = str(settings.infrastructure_config.redis_dsn)

celery_app = Celery("sales_llm")

celery_app.conf.update(
    broker_url = redis_url,
    result_backend = redis_url,
    accept_content = [
        'json',
        'application/json',
    ],
    timezone = 'UTC',
    enable_utc = True,
    task_track_started = True,
    worker_hijack_root_logger = False,
    worker_redirect_stdouts_level = 'ERROR',
    broker_connection_retry_on_startup = True,
)


@celery_app.task
def generate_prompt(llm_date: date):
    llm_service = LlmService()

    sales_service = SalesService()
    total_revenue = sales_service.get_total_revenue_by_date(llm_date)
    top_goods = sales_service.get_top_goods_by_date(llm_date)
    categories: list[str] = [category.get("categories") for category in top_goods]
    good_names: list[str] = [good_name.get("good_names") for good_name in top_goods]
    llm_service.create(llm_date, total_revenue, good_names, categories)
