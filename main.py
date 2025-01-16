import asyncio
import os
from structlog import get_logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.handlers import router
from src.gifts import get_client

from config import BOT_TOKEN


async def try_load_session():
    if 'main.session' not in os.listdir('session'):
        await get_client()

async def startup_info(bot: Bot):
    logger = get_logger()
    me = await bot.get_me()

    await logger.ainfo(f'start bot: @{me.username} [developer: t.me/awixa]')

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
        parse_mode='html'
    ))

    dp = Dispatcher()
    dp.include_router(router)

    await try_load_session()
    await startup_info(bot)
    await dp.start_polling(bot) 


if __name__ == '__main__':
    asyncio.run(main())