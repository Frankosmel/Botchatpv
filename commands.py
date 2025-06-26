from aiogram.filters import Command
from json_utils import read_json
from config import ADMINS

@startup_handler.message(Command("comandos"))
async def mostrar_comandos(msg: types.Message):
    users = read_json("users.json")
    user_id = msg.from_user.id

    # Si es Admin
    if user_id in ADMINS:
        await msg.answer(
            "🛠️ <b>Comandos para Administradores:</b>\n"
            "/admin – Abrir panel de administración\n"
            "/planes – Ver opciones de pago\n"
            "/comandos – Ver este mensaje",
            parse_mode="HTML"
        )
        return

    # Buscar rol por business_connection_id
    user_role = "normal"
    for bcid, data in users.items():
        if data["user_id"] == user_id:
            exp = data.get("expires_at")
            if exp:
                dias = (datetime.strptime(exp, "%Y-%m-%d") - datetime.now()).days
                if dias >= 30:
                    user_role = "premium elite"
                elif dias >= 15:
                    user_role = "premium plus"
                elif dias >= 7:
                    user_role = "premium básico"
                else:
                    user_role = "normal"
            break

    # Mensaje por tipo
    if user_role == "normal":
        texto = (
            "🧾 <b>Comandos disponibles:</b>\n"
            "/planes – Ver precios y métodos de pago\n"
            "/comandos – Mostrar comandos"
        )
    else:
        texto = (
            f"🏆 <b>Bienvenido, usuario {user_role.upper()}!</b>\n\n"
            "🤖 Tu cuenta responde automáticamente a tus clientes.\n"
            "🧠 Puedes usar:\n"
            "/prompt – Cambiar la forma en que responde ChatGPT\n"
            "/apikey – Cambiar tu API key de OpenAI\n"
            "/comandos – Mostrar comandos"
        )
    await msg.answer(texto, parse_mode="HTML")
