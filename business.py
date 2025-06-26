from aiogram import Router, Bot, types, F
from aiogram.enums import ParseMode
from json_utils import read_json, write_json

business_handlers = Router()
USERS_FILE = "users.json"

# Detección de conexión Business
@business_handlers.update(F.business_connection)
async def handle_business_connection(update: types.Update, bot: Bot):
    bc = update.business_connection
    user_id = bc.user.id
    username = bc.user.username or f"ID:{user_id}"
    bc_id = bc.id

    users = read_json(USERS_FILE)

    # Guardar conexión si es nueva
    if bc_id not in users:
        users[bc_id] = {
            "user_id": user_id,
            "username": username,
            "prompt": "",
            "openai_key": "",
            "expires_at": None
        }
        write_json(USERS_FILE, users)

        await bot.send_message(
            chat_id=bc.user_chat_id,
            text=(
                f"✅ Tu cuenta Business ha sido conectada correctamente.\n\n"
                f"👤 Usuario: @{username}\n"
                f"🧾 ID Business: <code>{bc_id}</code>\n\n"
                "✏️ Por favor, escribe el prompt que quieres usar con ChatGPT.\n"
                "Ejemplo: <i>Responde como un vendedor profesional de tecnología en Cuba</i>"
            ),
            parse_mode=ParseMode.HTML
        )
    else:
        await bot.send_message(
            chat_id=bc.user_chat_id,
            text="👋 Ya estás conectado. Si deseas cambiar tu prompt o API key, escribe /prompt o /apikey."
        )


# Capturar prompt personalizado
@business_handlers.message(F.text.startswith("Responde") | F.text.startswith("Eres") | F.text.startswith("Actúa"))
async def set_prompt(msg: types.Message):
    users = read_json(USERS_FILE)
    found = False
    for bc_id, data in users.items():
        if data["user_id"] == msg.from_user.id:
            data["prompt"] = msg.text.strip()
            write_json(USERS_FILE, users)
            found = True
            break

    if found:
        await msg.reply(
            "✅ Tu prompt fue guardado exitosamente.\n\n"
            "Ahora envía tu API key de OpenAI (formato: <code>sk-xxxxxx</code>)"
        )
    else:
        await msg.reply("❌ No encontré tu cuenta Business registrada. Conéctala desde los ajustes de Telegram Business.")


# Capturar API key de OpenAI
@business_handlers.message(F.text.startswith("sk-"))
async def set_apikey(msg: types.Message):
    users = read_json(USERS_FILE)
    found = False
    for bc_id, data in users.items():
        if data["user_id"] == msg.from_user.id:
            data["openai_key"] = msg.text.strip()
            write_json(USERS_FILE, users)
            found = True
            break

    if found:
        await msg.reply("🔐 Tu API key fue guardada correctamente.\n\n✅ El sistema ya está listo para responder con ChatGPT.")
    else:
        await msg.reply("❌ No encontré tu cuenta Business registrada.")
