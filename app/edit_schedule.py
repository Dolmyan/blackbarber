import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.book_service import get_weekday_name, get_weekday_name_imen
from config import *
from database import BotDB
from states import Form

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)

@router.message(F.text == 'Изменить расписание')
async def edit_services(message: Message, state: FSMContext):
    if message.from_user.id==admin_id:
        await message.answer('Функция скоро будет добавлена')