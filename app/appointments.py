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

@router.callback_query(lambda c: c.data.startswith("admin_confirm_"))
async def admin_confirm_callback(callback_query: CallbackQuery):
    appointment_id = int(callback_query.data.removeprefix("admin_confirm_"))
    success = db.confirm_appointment(appointment_id)

    await callback_query.message.edit_reply_markup()

    if success:
        await callback_query.message.answer(f"✅ Запись #{appointment_id} успешно подтверждена.")
    else:
        await callback_query.message.answer(f"❌ Ошибка: запись #{appointment_id} не найдена или уже подтверждена.")


@router.callback_query(lambda c: c.data.startswith("admin_cancel_"))
async def admin_cancel_callback(callback_query: CallbackQuery):
    appointment_id = int(callback_query.data.removeprefix("admin_cancel_"))
    success=db.cancel_appointment(appointment_id)

    await callback_query.message.edit_reply_markup()
    if success:
        await callback_query.message.answer(f"✅ Запись #{appointment_id} успешно ОТМЕНЕНА.")
    else:
        await callback_query.message.answer(f"❌ Ошибка отмены: запись #{appointment_id} не найдена или уже отменена.")
