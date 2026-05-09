from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.database_config import DATABASE_CONFIG

app = FastAPI()

register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=False, # Use False if using Aerich for migrations
    add_exception_handlers=True,
)
