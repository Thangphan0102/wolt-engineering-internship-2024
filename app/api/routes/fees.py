from fastapi import APIRouter


router = APIRouter()


@router.post("/")
def calculate_fee():
    return {"delivery_fee": 710}
