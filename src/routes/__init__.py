from src.routes.main import router as main_router
from src.routes.fanuc import router as fanuc_router
from src.routes.video import router as video_router


def register_routes(app):
    app.include_router(main_router)
    app.include_router(fanuc_router, prefix='/fanuc')
    app.include_router(video_router, prefix='/video')
