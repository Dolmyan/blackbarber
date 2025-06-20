import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import *
from database import BotDB

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)


def get_weekday_name(day_number: int) -> str:
    days = {
        1: "понедельник",
        2: "вторник",
        3: "среду",
        4: "четверг",
        5: "пятницу",
        6: "субботу",
        7: "воскресенье"
    }
    return days.get(day_number)


def get_weekday_name_imen(day_number: int) -> str:
    weekdays = {
        1: "Понедельник",
        2: "Вторник",
        3: "Среда",
        4: "Четверг",
        5: "Пятница",
        6: "Суббота",
        7: "Воскресенье"
    }
    return weekdays.get(day_number)


def get_available_time_keyboard(available_times, data=None):
    keyboard = []
    row = []

    for i, time_slot in enumerate(available_times, 1):
        button = InlineKeyboardButton(
                text=time_slot,
                callback_data=f"time_{time_slot.replace(':', '').replace(' ', '').replace('-', '_')}"
        )
        row.append(button)
        if len(row) == 2:  # по 2 кнопки в ряд
            keyboard.append(row)
            row = []

    if row:  # добавим оставшиеся кнопки, если есть
        keyboard.append(row)
    if data:
        keyboard.append([
            InlineKeyboardButton(text="🔙 К выбору дня", callback_data=f"selected_service_{data.get('service')}"),
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(F.text == 'Записаться на услугу')
async def book_service(message: Message, state: FSMContext):
    services = db.get_services()
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=service, callback_data=f"selected_service_{service}")]
                for service in services
            ]
    )

    await message.answer(
            "🛍️ <b>Выберите услугу:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
    )


@router.callback_query(lambda c: c.data in ["book_service"])
async def book_service(callback_query: CallbackQuery, state: FSMContext):
    services = db.get_services()
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=service, callback_data=f"selected_service_{service}")]
                for service in services
            ]
    )

    await callback_query.message.edit_text(
            "🛍️ <b>Выберите услугу:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
    )


@router.callback_query(lambda c: c.data.startswith("selected_service_"))
async def service_chosen(callback_query: CallbackQuery, state: FSMContext):
    service = callback_query.data.removeprefix("selected_service_")
    await state.update_data(service=service)
    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Понедельник", callback_data="day_1"),
            InlineKeyboardButton(text="Вторник", callback_data="day_2"),
            InlineKeyboardButton(text="Среда", callback_data="day_3"),
            InlineKeyboardButton(text="Четверг", callback_data="day_4")
        ],
        [
            InlineKeyboardButton(text="Пятница", callback_data="day_5"),
            InlineKeyboardButton(text="Суббота", callback_data="day_6"),
            InlineKeyboardButton(text="Воскресенье", callback_data="day_7")
        ],
        [
            InlineKeyboardButton(text="🔙 К выбору услуг", callback_data="book_service"),
        ]
    ])
    await callback_query.message.edit_text(
            "📆 <b>Выберите дату:</b>",
            reply_markup=button,
            parse_mode='HTML'
    )


@router.callback_query(lambda c: c.data.startswith('day_'))
async def day_chosen(callback_query: CallbackQuery, state: FSMContext):
    day = callback_query.data.removeprefix("day_")
    await state.update_data(day=day)
    day_name = get_weekday_name(int(day))

    available_times = db.get_available_times(day)
    data = await state.get_data()
    keyboard = get_available_time_keyboard(available_times=available_times, data=data)
    await callback_query.message.edit_text(
            f"📆 <b>Свободное время на {day_name}</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
    )


@router.callback_query(lambda c: c.data.startswith("time_"))
async def time_chosen(callback_query: CallbackQuery, state: FSMContext):
    raw_time = callback_query.data.removeprefix("time_")
    formatted_time = f"{raw_time[:2]}:{raw_time[2:]}"  # превращаем "1200" в "12:00"

    await state.update_data(time=formatted_time)



    keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📱 Отправить номер", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
    )

    await callback_query.message.answer(
            text="<b>📞 Для записи необходимо отправить номер телефона</b>\nНажмите кнопку ниже, чтобы поделиться своим контактом.",
            reply_markup=keyboard,
            parse_mode='HTML'
    )


@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    contact = message.contact
    user_id = message.from_user.id
    await state.update_data(phone_number=contact.phone_number)


    data = await state.get_data()
    service = data.get("service")
    time=data.get("time")
    day = get_weekday_name_imen(int(data.get("day")))
    button = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Записаться на услугу")],
                [KeyboardButton(text="Связаться с мастером")],
            ], resize_keyboard=True
    )
    await message.answer(text='Контакт успешно получен!',reply_markup=button)
    await message.answer(
        f"<b>Подтверждение записи</b>\n"
        f"💇 Услуга: {service}\n"
        f"📆 День: {day}\n"
        f"🕐 Время: {time}\n\n"
        f"Подтвердить запись?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_booking")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"day_{data.get('day')}")]
        ]),
        parse_mode='HTML',
)

@router.callback_query(lambda c: c.data in ["confirm_booking"])
async def time_chosen(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    service = data.get("service")
    time = data.get("time")
    day = get_weekday_name_imen(int(data.get("day")))


    print(data)
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username or ""
    first_name = callback_query.from_user.first_name or ""
    last_name = callback_query.from_user.last_name or ""

    service = data.get("service")
    day = int(data.get("day"))
    time = data.get("time")
    phone_number = data.get("phone_number")
    appointment_id=db.add_appointment(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        service=service,
        day_of_week=day,
        time=time,
        phone_number=phone_number
    )
    button2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить запись", callback_data=f"admin_cancel_{appointment_id}")],
    ])
    await callback_query.message.edit_text(text='Запись подтверждена! Ожидайте напоминания\n'
        f"💇 Услуга: {service}\n"
        f"📆 День: {day}\n"
        f"🕐 Время: {time}\n\n", reply_markup=button2)

    full_name = f"{first_name} {last_name}".strip()
    tg_profile = f"@{username}" if username else f"<code>{user_id}</code>"

    text = (
        "<b>📥 Новая запись</b>\n\n"
        f"<b>Клиент:</b> {full_name}\n"
        f"<b>Профиль:</b> {tg_profile}\n"
        f"<b>Телефон:</b> {phone_number}\n"
        f"<b>ID:</b> {appointment_id}\n\n"

        f"<b>Услуга:</b> {service}\n"
        f"<b>День:</b> {get_weekday_name_imen(day)}\n"
        f"<b>Время:</b> {time}"
    )

    button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin_confirm_{appointment_id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data=f"admin_cancel_{appointment_id}")
        ],
    ])

    await bot.send_message(chat_id=admin_id, text=text, reply_markup=button, parse_mode="HTML")