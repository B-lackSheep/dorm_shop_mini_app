import asyncio
import logging
from config import bot, dp
from handlers import get_all_routers


logger = logging.getLogger(__name__)


def start_bot_polling():

    async def main():
        for router in get_all_routers():
            dp.include_router(router)

        await dp.start_polling(bot)

    asyncio.run(main())
