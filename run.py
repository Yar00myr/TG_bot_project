import logging
import asyncio
import sys
from bot import start
from db import migrate


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    migrate()
    asyncio.run(start())
