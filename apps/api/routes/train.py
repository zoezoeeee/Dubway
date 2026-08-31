from fastapi import APIRouter

from services.gtfs import get_live_train_response

router = APIRouter()


@router.get("/live/train")
def live_train(station_code: str):
    return get_live_train_response(station_code)
