from aiogram import Router, Bot, types, F
from aiogram.enums import ParseMode
from json_utils import read_json, write_json
import openai

business_handlers = Router()
USERS_FILE = "users.json"

# 🟢 1. Detectar nueva conexión Business
@business_handlers.update(F.business_connection)
async def handle_business_connection(update: types.Update, bot: Bot):
    bc = update.business_connection
    user_id = bc.user.id
    username = bc.user.username or f"ID:{user_id}"
    bc_id = bc.id

    users = read_json(USERS_FILE)

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
                "✏️ Ahora escribe el prompt que quieres usar con ChatGPT.\n"
                "Ejemplo: <i>Responde como un vendedor profesional de tecnología en Cuba</i>"
            ),
            parse_mode=ParseMode.HTML
        )
    else:
        await bot.send_message(
            chat_id=bc.user_chat_id,
            text="👋 Ya estás conectado. Si deseas cambiar tu prompt o API key, escribe /prompt o /apikey."
        )

# 🟡 2. Guardar Prompt personalizado
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
            "Ahora envía tu API key de OpenAI (formato: <code>sk-xxxxxx</code>)",
            parse_mode=ParseMode.HTML
        )
    else:
        await msg.reply("❌ No encontré tu cuenta Business registrada. Conéctala desde los ajustes de Telegram Business.")

# 🟠 3. Guardar API Key personalizada
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

# 🔵 4. Responder automáticamente a mensajes Business
@business_handlers.update(F.business_message)
async def handle_business_message(update: types.Update, bot: Bot):
    msg = update.business_message
    bc_id = msg.business_connection_id
    chat_id = msg.chat.id
    text = msg.text

    users = read_json(USERS_FILE)
    user_data = users.get(bc_id)

    if not user_data:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Esta cuenta Business no está registrada correctamente.",
            business_connection_id=bc_id
        )
        return

    prompt = user_data.get("prompt", "")
    apikey = user_data.get("openai_key", "")

    if not prompt or not apikey:
        await bot.send_message(
            chat_id=chat_id,
            text="⚠️ Esta cuenta aún no tiene prompt o API Key configurada. No puedo responder.",
            business_connection_id=bc_id
        )
        return

    # Llamar a OpenAI
    try:
        openai.api_key = apikey
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        await bot.send_message(
            chat_id=chat_id,
            text=f"❌ Error al procesar con OpenAI:\n<code>{str(e)}</code>",
            business_connection_id=bc_id,
            parse_mode=ParseMode.HTML
        )
        return

    # Responder como cuenta Business
    await bot.send_message(
        chat_id=chat_id,
        text=reply,
        business_connection_id=bc_id
    )
