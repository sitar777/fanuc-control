from fastapi import Request, status, APIRouter

from src.config import settings

router = APIRouter()


@router.get('/version', status_code=status.HTTP_200_OK)
def get_version(request: Request):
    return {'version': {settings.VERSION}}
