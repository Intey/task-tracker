import typing as t
from uuid import uuid4

from task_tracker.storage import Storage
from loguru import logger


async def post(body):
    logger.debug(f"{body}")
    egrees = Storage()
    logger.debug("save issue to cache")
    key = uuid4().hex[:7]
    await egrees.create_issue(key, body)
    logger.debug("issue request cached")
    return {"key": key}


async def search(skilled, estimated, priority):
    egrees = Storage()
    logger.debug("search issues")
    results = await egrees.get_issues()
    logger.debug(f"got results from db {results}",)
    return {"issues": results}


async def gantt():
    egrees = Storage()
    issues = await egrees.get_issues()
