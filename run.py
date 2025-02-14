import logging
import asyncio
import sys
from bot import start
from db import AsyncDB


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await AsyncDB.migrate()
    await start()


if __name__ == "__main__":
    asyncio.run(main())
