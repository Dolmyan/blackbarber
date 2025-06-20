import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.view_appointments import format_appointments_list
from config import *
from database import BotDB
from states import Form

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)

@router.message(F.text == 'Отменить запись')
async def cancel_appointment(message: Message, state: FSMContext):
    if message.from_user.id == admin_id:
        appointments = db.get_all_appointments()
        text = format_appointments_list(appointments)
        await message.answer(text, parse_mode="HTML")
        await message.answer(text='Введите номер записи, которую хотите отменить', parse_mode="HTML")
        await state.set_state(Form.input_cancel)

@router.message(Form.input_cancel)
async def input_cancel(message: Message, state: FSMContext):
    if message.from_user.id != admin_id:
        return

    appointment_id_text = message.text.strip()

    if not appointment_id_text.isdigit():
        await message.answer("❌ Введите корректный номер записи (целое число).")
        return

    appointment_id = int(appointment_id_text)

    success = db.cancel_appointment(appointment_id)

    if success:
        await message.answer(f"✅ Запись #{appointment_id} успешно отменена.")
    else:
        await message.answer(f"❌ Запись с ID {appointment_id} не найдена или уже отменена.")

    await state.clear()