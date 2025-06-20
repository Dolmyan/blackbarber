import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import *
from database import BotDB
from states import Form

db = BotDB('blackbarber.db')
router = Router()
bot = Bot(token=TG_TOKEN)

logger = logging.getLogger(__name__)


def get_weekday_number(day_name: str) -> int | None:
    weekdays = {
        "понедельник": 1,
        "вторник": 2,
        "среда": 3,
        "четверг": 4,
        "пятница": 5,
        "суббота": 6,
        "воскресенье": 7
    }
    return weekdays.get(day_name.strip().lower())


@router.message(F.text == 'Добавить запись')
async def add_appointment(message: Message, state: FSMContext):
    await message.answer(
            text=(
                "Введите данные в формате:\n\n"
                "<b>Услуга, День недели, Время, Имя, Номер</b>\n\n"
                "Например:\n"
                "<code>Стрижка, вторник, 14:00, Алексей, 89034193259</code>"
            ),
            parse_mode='HTML'
    )
    await state.set_state(Form.input_contact)


@router.message(Form.input_contact)
async def get_contact(message: Message, state: FSMContext):
    try:
        service, day_str, time, first_name, phone = map(str.strip, message.text.split(","))
        day = get_weekday_number(day_str)  # например: "Вторник" -> 2

        if day is None:
            await message.answer("Неверный день недели. Попробуйте снова.")
            return

        username = 'None'
        user_id = message.from_user.id
        last_name = 'None'  # если не вводим

        appointment_id = db.add_appointment(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                service=service,
                day_of_week=day,
                time=time,
                phone_number=phone
        )

        await message.answer(
                text=(
                    f"Проверьте данные\n\n"
                    f"<b>Услуга:</b> {service}\n"
                    f"<b>День:</b> {day}, <b>время:</b> {time}\n"
                    f"<b>Имя:</b> {first_name} {last_name or ''}\n"
                    f"<b>Номер:</b> {phone}"),
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin_confirm_{appointment_id}"),
                        InlineKeyboardButton(text="❌ Отменить", callback_data=f"admin_cancel_{appointment_id}")
                    ]
                ])
        )

    except Exception as e:
        await message.answer("Произошла ошибка при обработке данных. Убедитесь, что вы ввели их в правильном формате.")
        print(f"Ошибка при разборе данных: {e}")
