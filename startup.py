from aiogram import Router, types
from aiogram.filters import CommandStart

startup_handler = Router()

@startup_handler.message(CommandStart())
async def start(msg: types.Message):
    await msg.answer(
        "👋 ¡Bienvenido al Bot de Atención Business!\n\n"
        "🔌 Usa este bot para conectar tu perfil de Telegram Business y activar respuestas automáticas "
        "con tu propia API de ChatGPT. Más módulos pronto..."
    )
