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

@router.message(F.text == 'Изменить услуги')
async def edit_services(message: Message, state: FSMContext):
    if message.from_user.id==admin_id:
        services = db.get_services()
        keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    *[
                        [InlineKeyboardButton(text=service, callback_data=f"selected_service_{service}")]
                        for service in services
                    ],
                    [InlineKeyboardButton(text="➕ Добавить услугу", callback_data="add_service"),
                    InlineKeyboardButton(text="➖ Удалить услугу", callback_data="remove_service")],
                ]
        )

        await message.answer(
                "🛍️ <b>Актуальные услуги:</b>",
                reply_markup=keyboard,
                parse_mode='HTML'
        )

@router.callback_query(lambda c: c.data in ["add_service"])
async def add_service(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите название новой услуги:")
    await state.set_state(Form.input_new_service)

@router.message(Form.input_new_service)
async def process_new_service(message: Message, state: FSMContext):
    new_service = message.text.strip()

    if not new_service:
        await message.answer("❗ Название услуги не может быть пустым. Попробуйте снова.")
        return

    db.add_service(new_service)
    await message.answer(f"✅ Услуга <b>{new_service}</b> добавлена!", parse_mode="HTML")
    services = db.get_services()
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                *[
                    [InlineKeyboardButton(text=service, callback_data=f"selected_service_{service}")]
                    for service in services
                ],
                [InlineKeyboardButton(text="➕ Добавить услугу", callback_data="add_service"),
                 InlineKeyboardButton(text="➖ Удалить услугу", callback_data="remove_service")],
            ]
    )

    await message.answer(
            "🛍️ <b>Актуальные услуги:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
    )

@router.callback_query(lambda c: c.data in ["remove_service"])
async def remove_service_callback(callback: CallbackQuery, state: FSMContext):
    services = db.get_services()

    if not services:
        await callback.message.answer("❗ Услуг для удаления нет.")
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=service, callback_data=f"remove_{service}")]
                for service in services
            ]
    )
    await callback.message.answer(
            "Выберите услугу для удаления:",
            reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data.startswith("remove_"))
async def process_service_removal(callback: CallbackQuery):
    service_to_remove = callback.data.removeprefix("remove_")

    db.remove_service(service_to_remove)
    await callback.message.edit_text(
        f"🗑️ Услуга <b>{service_to_remove}</b> удалена.",
        parse_mode="HTML"
    )
    services = db.get_services()
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                *[
                    [InlineKeyboardButton(text=service, callback_data=f"selected_service_{service}")]
                    for service in services
                ],
                [InlineKeyboardButton(text="➕ Добавить услугу", callback_data="add_service"),
                 InlineKeyboardButton(text="➖ Удалить услугу", callback_data="remove_service")],
            ]
    )

    await callback.message.answer(
            "🛍️ <b>Актуальные услуги:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
    )