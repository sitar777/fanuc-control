from fastapi import FastAPI
from uvicorn import run

import src.routes as routes
from src.config import settings


app = FastAPI()
app.fanuc_position = settings.FANUC_HOME

routes.register_routes(app)

if __name__ == '__main__':
    run('main:app', port=5000, reload=True)
