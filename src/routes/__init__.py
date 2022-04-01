from src.routes.main import router as main_router
from src.routes.fanuc import router as fanuc_router


def register_routes(app):
    app.include_router(main_router)
    app.include_router(fanuc_router, prefix='/fanuc')
