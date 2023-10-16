from contextlib import asynccontextmanager

import asyncpg
import grpc
from loguru import logger


@asynccontextmanager
async def ErrorAsyncContextManager(context: any) -> asyncpg.Connection:
    try:
        yield None
    except Exception as e:
        message = type(e).__name__ + ": " + str(e)
        logger.error(message)
        await context.abort(grpc.StatusCode.UNKNOWN, message)
