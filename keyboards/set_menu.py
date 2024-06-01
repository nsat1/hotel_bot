from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command='/help', description='Справка по работе бота'),
        BotCommand(
            command='/custom', description='Выбор отеля по пользовательским настройкам'),
        BotCommand(
            command='/high', description='Выбор отеля премиум класса'),
        BotCommand(
            command='/low', description='Выбор недорого отеля')
    ]
    await bot.set_my_commands(main_menu_commands)
