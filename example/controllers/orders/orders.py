from fastapi import APIRouter

router = APIRouter()


@router.get("/orders")
def list_orders():
    return [{"id": 1, "item": "Book"}, {"id": 2, "item": "Pen"}]
