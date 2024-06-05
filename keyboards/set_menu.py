from aiogram import Bot
from aiogram.types import BotCommand
from fluentogram import TranslatorRunner


async def get_translated_commands(i18n: TranslatorRunner):
    main_menu_commands = [
        BotCommand(
            command='/help', description=i18n.help.command.description()),
        BotCommand(
            command='/custom', description=i18n.custom.command.description()),
        BotCommand(
            command='/high', description=i18n.high.command.description()),
        BotCommand(
            command='/low', description=i18n.low.command.description())
    ]
    return main_menu_commands


async def set_main_menu(bot: Bot, i18n: TranslatorRunner):
    main_menu_commands = await get_translated_commands(i18n)
    await bot.set_my_commands(main_menu_commands)
