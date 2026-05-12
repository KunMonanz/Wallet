from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "blacklistedtoken" (
    "id" UUID NOT NULL PRIMARY KEY,
    "jti" VARCHAR(100) NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "blacklistedtoken";"""


MODELS_STATE = (
    "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"
)
