import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from startup import startup_handler
from business import business_handlers
from admin_panel import admin_router
from scheduler import start_scheduler

# Inicializa bot y dispatcher
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Registra todos los handlers
dp.include_routers(
    startup_handler,
    business_handlers,
    admin_router
)

# Inicia todo
if __name__ == "__main__":
    start_scheduler(bot)
    asyncio.run(dp.start_polling(bot))
