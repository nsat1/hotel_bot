from datetime import datetime, date

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State, StateFilter
from aiogram.fsm.state import default_state

from aiogram_dialog import Window, Dialog, DialogManager, StartMode, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Back, Next, Calendar
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.input import TextInput

from models.users import User
from db.base_repository import BaseRepository


users = BaseRepository(User)

user_router = Router()


class DialogSG(StatesGroup):
    start = State()
    city_choose = State()
    date_in = State()
    date_out = State()
    choice_result = State()


async def getter(dialog_manager: DialogManager, **kwargs):
    context = dialog_manager.current_context()
    return {
        "city": dialog_manager.find("city").get_value(),
        "date_in": context.dialog_data.get("date_in"),
        "date_out": context.dialog_data.get("date_out"),
    }


async def start_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer("Отлично")
    await manager.next()


async def on_city_entered(message: Message, widget: TextInput, manager: DialogManager, input: str):
    manager.current_context().dialog_data["city"] = input
    await manager.next()


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.current_context().dialog_data["date_in"] = str(selected_date)
    await callback.answer(f"Дата заезда: {selected_date}")
    await manager.next()


async def out_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.current_context().dialog_data["date_out"] = str(selected_date)
    await callback.answer(f"Дата выезда: {selected_date}")
    await manager.next()


dialog = Dialog(
    Window(
        Format("Добрый день"),
        Button(Const("Начнем поиск"), id="start_search", on_click=start_clicked),
        state=DialogSG.start
    ),
    Window(
        Format("Выберите город"),
        TextInput(
            id="city",
            on_success=Next(),
        ),
        state=DialogSG.city_choose
    ),
    Window(
        Format("Выберите дату заезда"),
        Calendar(id="date_in", on_click=on_date_selected),
        Back(text=Const("Вернуться к выбору города")),
        state=DialogSG.date_in
    ),
    Window(
        Format("Выберите дату выезда"),
        Calendar(id="date_out", on_click=out_date_selected),
        Back(text=Const("Вернуться к дате заезда")),
        state=DialogSG.date_out
    ),
    Window(
        Jinja(
            "<b>Вы выбрали</b>:\n\n"
            "<b>Город</b>: {{city}}\n"
            "<b>Дата заезда</b>: {{date_in}}\n"
            "<b>Дата выезда</b>: {{date_out}}\n"
        ),
        state=DialogSG.choice_result,
        getter=getter,
        parse_mode="html"
    )
)

user_router.include_router(dialog)


@user_router.message(Command("start"), StateFilter(default_state))
async def cmd_start(message: Message, dialog_manager: DialogManager):

    user_id = message.from_user.id

    existing_user = await users.get(user_id)

    if not existing_user:
        new_user_data = {
            "id": user_id,
            "fullname": message.from_user.full_name,
            "username": message.from_user.username,
            "created_at": datetime.now(),
            "language_code": message.from_user.language_code
            }
        await users.create(**new_user_data)
    await dialog_manager.start(DialogSG.start, mode=StartMode.RESET_STACK)

setup_dialogs(user_router)
