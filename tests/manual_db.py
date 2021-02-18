import asyncio

import loguru
from motor.motor_asyncio import AsyncIOMotorClient


async def manual():
    cli = AsyncIOMotorClient("localhost", 27017)
    loguru.logger.debug("run insert")
    await cli.first_database.issues.insert_one({"summary": "example"})
    loguru.logger.debug("done")


asyncio.run(manual())
