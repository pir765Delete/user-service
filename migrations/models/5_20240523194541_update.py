from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" ADD "leader" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "subdivision" DROP COLUMN "leader";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" DROP COLUMN "leader";
        ALTER TABLE "subdivision" ADD "leader" INT NOT NULL;"""
