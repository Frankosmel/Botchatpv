import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from startup import startup_handler
from business import business_handlers

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Registrar routers
dp.include_routers(startup_handler, business_handlers)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
