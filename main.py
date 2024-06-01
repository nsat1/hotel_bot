import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import settings

from fluentogram import TranslatorHub

from handlers import routers_list

from keyboards.set_menu import set_main_menu

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

    dp = Dispatcher()

    translator_hub: TranslatorHub = create_translator_hub()

    dp.include_routers(*routers_list)

    @dp.message.middleware()
    async def translator_middleware(handler, event, data):
        return await TranslatorRunnerMiddleware(translator_hub)(handler, event, data)

    await init_db()

    await dp.start_polling(bot)
    await set_main_menu(bot)

asyncio.run(main())
