import json

import aioredis
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient


class Storage:
    def __init__(self):
        logger.debug("initialize database client")
        self.__db = None

    async def create_issue(self, key: str, payload: dict):
        db = await self.__get_db()
        await db.hset("issues", key, json.dumps(payload))

    async def update_issue(self, key: str, payload: dict):
        db = await self.__get_db()
        value = await db.hget("issues", key)
        return value

    async def get_issues(self):
        db = await self.__get_db()
        kvals = await db.hgetall("issues")
        result = []
        for k, v in kvals.items():
            issue = json.loads(v)
            issue["key"] = k.decode("utf8")
            result.append(issue)
        return result

    async def __get_db(self):
        if self.__db is None:
            redis = await aioredis.create_redis_pool("redis://localhost")
            self.__db = redis
        return self.__db


class MongoStorage:
    def __init__(self):
        logger.debug("initialize database client")
        self.__db = None

    async def create_issue(self, key: str, payload: dict):
        db = await self.__get_db()
        payload["key"] = key
        await db.insert_one(payload)

    async def update_issue(self, key: str, payload: dict):
        db = await self.__get_db()
        pass

    async def get_issues(self):
        db = await self.__get_db()
        pass

    async def __get_db(self):
        if self.__db is None:
            client = AsyncIOMotorClient("localhost", 27017)
            self.__db = client.issues
        return self.__db


class MemoryStorage:
    def __init__(self):
        logger.debug("initialize database client")
        self.issues = {}

    async def create_issue(self, key: str, payload: dict):
        payload["key"] = key
        self.issues[key] = payload

    async def update_issue(self, key: str, payload: dict):
        exists = self.issues.get(key)
        if exists:
            self.issues[key] = payload
        else:
            raise ValueError("issue not exists")

    async def get_issues(self):
        return list(self.issues.values())
