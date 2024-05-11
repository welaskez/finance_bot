from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import router
from config import BOT_TOKEN

import asyncio
import logging


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
