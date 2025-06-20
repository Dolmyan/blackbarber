import logging
import asyncio
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
# from aiohttp_socks import ProxyConnector
from aiogram.fsm.storage.memory import MemoryStorage

from config import TG_TOKEN
from app.start import router
from app.contact_master import router as contact_master
from app.book_service import router as book_service
from app.view_appointments import router as view_appointments
from app.appointments import router as appointments
from app.admin_add_appointment import router as admin_add_appointment
from app.admin_cancel_appointment import router as admin_cancel_appointment
from app.support import router as support
from app.edit_services import router as edit_services
from app.edit_schedule import router as edit_schedule



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TG_TOKEN)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.include_router(contact_master)
    dp.include_router(book_service)
    dp.include_router(view_appointments)
    dp.include_router(appointments)
    dp.include_router(admin_add_appointment)
    dp.include_router(admin_cancel_appointment)
    dp.include_router(support)
    dp.include_router(edit_services)
    dp.include_router(edit_schedule)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


