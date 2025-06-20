import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import *
from database import BotDB

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    button = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Записаться на услугу")],
                [KeyboardButton(text="Связаться с мастером")],
            ], resize_keyboard=True
    )
    if message.from_user.id==admin_id:
        button = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Просмотреть записи")],
                    [KeyboardButton(text="Добавить запись"),
                     KeyboardButton(text="Отменить запись")],
                    [KeyboardButton(text="Изменить расписание"),
                    KeyboardButton(text="Изменить услуги"),

                    KeyboardButton(text="Тех. Поддержка")],

                ],
                resize_keyboard=True
        )

        await message.answer(
                "Добро пожаловать в меню администратора",
                reply_markup=button
        )
    else:
        await message.answer(
                "<b>👋 Привет!</b>\n"
                "Я бот для <b>записи на услуги</b>. Выбери, что хочешь сделать из меню ниже 👇",
                reply_markup=button,
                parse_mode='HTML'
        )

    await state.clear()




@router.message(Command('about'))
async def cmd_about(message: Message, state: FSMContext):
    text = (
        "<b>Бот для записи</b> к барберу 💈\n\n"
        "Разработчик: <a href='https://t.me/bigboyandroid'>@bigboyandroid</a>\n"
        "По вопросам сотрудничества и поддержки — пишите в личные сообщения."
    )
    await message.answer(text=text, parse_mode='HTML')