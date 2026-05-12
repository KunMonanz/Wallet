from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.database_config import TORTOISE_CONFIG
from user_app.routers import router as user_router
from wallet_app.routers import router as wallet_router

app = FastAPI()

app.include_router(
    user_router,
)
app.include_router(
    wallet_router,
)

register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)
