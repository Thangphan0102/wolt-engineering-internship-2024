from typing import Any

from fastapi import APIRouter

from app.schemas.fees import FeeCalculatorRequest, FeeCalculatorResponse
from app.utils.fee_calculator import FeeCalculator

router = APIRouter()

fee_calculator = FeeCalculator()


@router.post("/calculate_fee", response_model=FeeCalculatorResponse)
def calculate_fee(request: FeeCalculatorRequest) -> Any:
    delivery_fee = fee_calculator.calculate_delivery_fee(**request.model_dump())
    return FeeCalculatorResponse(delivery_fee=delivery_fee)
