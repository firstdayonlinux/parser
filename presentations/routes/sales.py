from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Annotated
from starlette import status

from presentations.schemas.common import Message
from presentations.schemas.sales import SalesResponse
from services.sales_service import SalesService

from background.celery_app import generate_prompt


router = APIRouter()


@router.post(
    "/create_prompt/",
    response_model=list[SalesResponse],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Message},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    },
)
async def create_prompt_from_file(file: Annotated[UploadFile, File(...)]) -> list[SalesResponse]:
    if not file.filename.endswith(".xml"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format")
    service = SalesService()
    file_content = await file.read()
    parsed_data = service.parse_xml(file_content)
    result = service.batch_create(parsed_data)
    result = [
        SalesResponse(
            id=res.id,
            good_name=res.good_name,
            amount=res.amount,
            price=res.price,
            sales_date=res.sales_date,
        ) for res in result
    ]
    generate_prompt.delay(result[0].sales_date)
    return result
