import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from redis.asyncio import Redis

from fluentogram import TranslatorHub

from handlers import routers_list
from config_data.config import settings
from middlewares.i18n import TranslatorRunnerMiddleware
from utils.i18n import create_translator_hub
from db.init_db import init_db


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot...')

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))

    dp = Dispatcher(storage=storage)

    translator_hub: TranslatorHub = create_translator_hub()

    dp.include_routers(*routers_list)

    @dp.message.middleware()
    async def translator_middleware(handler, event, data):
        return await TranslatorRunnerMiddleware(translator_hub)(handler, event, data)

    await init_db()

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

asyncio.run(main())
