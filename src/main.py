from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
import uvicorn

from controllers import (
    auth,
    users_manager
)

app = FastAPI()

# DB Configs
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={
        "models": [
            "models.users"
        ]
    },
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/log")
def log_info():
    return {'info': 'running...'}  

app.include_router(
    auth.router,
    tags=['auth']
) 

app.include_router(
    users_manager.router,
    prefix='/account',
    tags=['account']
)

if __name__ == "__main__":
    uvicorn.run('main:app', port=5000, log_level='info', reload=True)   