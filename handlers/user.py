from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from fluentogram import TranslatorRunner

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, i18n: TranslatorRunner):
    username = html.quote(message.from_user.full_name)
    await message.answer(text=i18n.description(username=username))
