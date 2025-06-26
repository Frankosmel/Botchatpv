import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from startup import startup_handler
from business import business_handlers
from admin_panel import admin_router
from payment import payment_router
from profile_menu import profile_router
from scheduler import start_scheduler

# Inicializar bot y dispatcher
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Registrar todos los routers
dp.include_routers(
    startup_handler,
    business_handlers,
    admin_router,
    payment_router,
    profile_router
)

# Iniciar todo
if __name__ == "__main__":
    start_scheduler(bot)
    asyncio.run(dp.start_polling(bot))
