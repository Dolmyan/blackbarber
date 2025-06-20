import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.book_service import get_weekday_name, get_weekday_name_imen
from config import *
from database import BotDB

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)


def format_appointments_list(appointments: list) -> str:
    if not appointments:
        return "Записей пока нет."

    text = "<b>Список записей:</b>\n\n"
    for i, (service, day, time, phone_number, first_name, last_name, username, id) in enumerate(appointments, 1):
        full_name = (first_name or "") + (" " + last_name if last_name else "")
        full_name = full_name.strip() or "Неизвестно"
        tg_profile = f"@{username}" if username else "нет"
        day_name = get_weekday_name_imen(day)

        text += (
            f"🆔 {id}\n"
            f"💈 {service}\n"
            f"📅 {day_name}, 🕒 {time}\n"
            f"👤 {full_name} ({tg_profile})\n"
            f"📱 {phone_number or 'не указан'}\n\n"
        )
    return text


@router.message(lambda msg: msg.text == "Просмотреть записи")
async def view_appointments(message: Message):
    if message.from_user.id == admin_id:
        appointments = db.get_all_appointments()
        text = format_appointments_list(appointments)
        await message.answer(text, parse_mode="HTML")
