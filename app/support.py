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

@router.message(F.text == 'Тех. Поддержка')
async def support(message: Message, state: FSMContext):
    text = (
        "<b>📞 Тех. Поддержка</b>\n\n"
        "👨‍💻 Валерий\n"
        "📱 89034193259\n"
        "💬 Telegram: @Bigboyandroid"
    )
    await message.answer(text, parse_mode="HTML")
