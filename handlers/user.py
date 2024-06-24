from datetime import datetime, date

import aiohttp
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
from config_data.config import settings


users = BaseRepository(User)

user_router = Router()


class DialogSG(StatesGroup):
    start = State()
    city_choose = State()
    date_in = State()
    date_out = State()
    choice_result = State()
    user_choice = State()


async def getter(dialog_manager: DialogManager, **kwargs):
    context = dialog_manager.current_context()
    return {
        "city": dialog_manager.find("city").get_value(),
        "date_in": context.dialog_data.get("date_in"),
        "date_out": context.dialog_data.get("date_out"),
        "search_results": context.dialog_data.get("search_results"),
        "photo_list": context.dialog_data.get("photo_list")
    }


async def start_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer("Начинаем ... ")
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


async def search(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer("Начинаем поиск")

    city = manager.find("city").get_value()
    date_in = manager.dialog_data.get("date_in")
    date_out = manager.dialog_data.get("date_out")

    querystring = {
        "location": city,
        "checkIn": date_in,
        "checkOut": date_out,
        "currency": "rub",
        "limit": "25",
        "token": settings.HOTEL_API
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url="http://engine.hotellook.com/api/v2/cache.json", params=querystring) as response:
            data = await response.json()

    manager.dialog_data["search_results"] = data

    await manager.next()


async def cmd_low(callback: CallbackQuery, widget, manager: DialogManager):
    await callback.answer("Формируем данные")
    data = manager.dialog_data.get("search_results")

    sorted_data = sorted(data, key=lambda x: x['priceAvg'])[:5]

    result = [{
        "hotelId": item["hotelId"],
        "priceAvg": item["priceAvg"],
        "stars": item["stars"],
        "hotelName": item["hotelName"],
        "geo": item["location"]["geo"]
    } for item in sorted_data]

    manager.dialog_data["result"] = result

    photo_hotel_ids = ','.join(str(hotel['hotelId']) for hotel in result)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://yasen.hotellook.com/photos/hotel_photos?id={photo_hotel_ids}"
        ) as response:
            photos_data = await response.json()

    first_photo_ids = {hotel_id: photos[0] for hotel_id, photos in photos_data.items()}
    photo_list = list(first_photo_ids.values())

    for hotel in result:
        photo_id = photo_list.pop(0)
        photo_url = f"https://photo.hotellook.com/image_v2/limit/{photo_id}/800/520.auto"
        caption = (
            f"Отель: {hotel['hotelName']}\n"
            f"Адрес: {hotel['geo']}\n"
            f"Stars: {hotel['stars']}\n"
            f"Средняя стоимость: {hotel['priceAvg']} рублей\n"
        )
        await callback.message.answer_photo(photo=photo_url, caption=caption)


dialog = Dialog(
    Window(
        Format("Настоящий бот поможет подобрать отель в указанном городе по приемлемой цене."),
        Button(Const("Начнем поиск"), id="start_search", on_click=start_clicked),
        state=DialogSG.start
    ),
    Window(
        Format("Напишите в чат название города в котором будет осуществлен поиск."),
        TextInput(
            id="city",
            on_success=Next(),
        ),
        state=DialogSG.city_choose
    ),
    Window(
        Format("Выберите дату заезда"),
        Calendar(id="date_in", on_click=on_date_selected),
        Back(text=Const("<< Назад")),
        state=DialogSG.date_in
    ),
    Window(
        Format("Выберите дату выезда"),
        Calendar(id="date_out", on_click=out_date_selected),
        Back(text=Const("<< Назад")),
        state=DialogSG.date_out
    ),
    Window(
        Jinja(
            "<b>Вы выбрали</b>:\n\n"
            "<b>Город</b>: {{city}}\n"
            "<b>Дата заезда</b>: {{date_in}}\n"
            "<b>Дата выезда</b>: {{date_out}}\n"
        ),
        Button(Const("Верно, начинаем поиск"), id="search", on_click=search),
        Back(text=Const("<< Назад")),
        state=DialogSG.choice_result,
        getter=getter,
        parse_mode="html"
    ),
    Window(
        Format("Выберите подходящий варинат:"),
        Button(Const("Подобрать отели по выгодной цене"), id="low", on_click=cmd_low),
        Button(Const("Подобрать отели премиум класса"), id="high"),
        Button(Const("Подобрать отели по ценовому диапазону"), id="custom"),
        state=DialogSG.user_choice
    ),
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
