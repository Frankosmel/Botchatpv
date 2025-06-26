from aiogram import Router, types
from aiogram.filters import CommandStart
from config import ADMINS

startup_handler = Router()

@startup_handler.message(CommandStart())
async def start(msg: types.Message):
    bienvenida = (
        "👋 ¡Bienvenido a <b>Francho Shop Bot</b>!\n\n"
        "🤖 Este bot responde automáticamente a tus clientes desde tu perfil de Telegram Business "
        "usando la inteligencia de ChatGPT.\n\n"
        "🧠 Puedes configurar tu propio prompt y usar tu propia API key de OpenAI para personalizar cómo responde tu cuenta.\n\n"
        "💳 Para comenzar, consulta los planes disponibles con /planes\n"
        "📌 Luego conecta el bot en Telegram Business → Ajustes → Chatbots → escribe <code>@TuBot</code>\n\n"
        "❓ Usa /comandos para ver lo que puedes hacer."
    )
    await msg.answer(bienvenida, parse_mode="HTML")
