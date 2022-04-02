from fastapi import Request, status, APIRouter, HTTPException

from src.config import settings
from src.models.fanuc import FanucPoint, FanucMessage, FanucPointDelta
from src.utils.fanuc import send_message

router = APIRouter()


@router.post('/move', status_code=status.HTTP_200_OK)
def move_to_point(request: Request, point: FanucPoint, velocity: int = 200):
    msg = FanucMessage(point=point, velocity=velocity)

    response = send_message(msg.bytes)
    if 'ERROR' in response:
        raise HTTPException(status.HTTP_409_CONFLICT, response)
    request.app.fanuc_position = point
    return {'current_position': point.dict()}


@router.post('/home', status_code=status.HTTP_200_OK)
def move_to_home_point(request: Request, velocity: int = 200):
    msg = FanucMessage(point=settings.FANUC_HOME, velocity=velocity)

    response = send_message(msg.bytes)
    if 'ERROR' in response:
        raise HTTPException(status.HTTP_409_CONFLICT, response)
    request.app.fanuc_position = settings.FANUC_HOME
    return {'current_position': settings.FANUC_HOME.dict()}


@router.post('/delta', status_code=status.HTTP_200_OK)
def move_to_delta(request: Request, delta: FanucPointDelta, velocity: int = 200):
    point = request.app.fanuc_position.point_from_delta(delta)
    msg = FanucMessage(point=point, velocity=velocity)

    response = send_message(msg.bytes)
    if 'ERROR' in response:
        raise HTTPException(status.HTTP_409_CONFLICT, response)
    request.app.fanuc_position = point
    return {'current_position': point.dict()}
