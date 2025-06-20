import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import *
from database import BotDB

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)

@router.message(F.text=='Связаться с мастером')
async def contact_master(message: Message, state: FSMContext):
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Написать в Telegram", url=f"https://t.me/{telegram_username}")],
        [InlineKeyboardButton(text="💬 Написать в WhatsApp", url=f"https://wa.me/{whatsapp_number}")],
    ])
    await message.answer(
            text=f"<b>👩‍🎨 Ваш мастер:</b> {master_first_name} {master_last_name}\n"
                 f"<b>📍 Место:</b> {master_location}\n"
                 f"<b>📞 Телефон:</b> {master_phone_number}",
            parse_mode='HTML',
            reply_markup=button
    )


