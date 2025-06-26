from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from json_utils import read_json, write_json

profile_router = Router()
USERS_FILE = "users.json"

# Comando para abrir menú de perfil
@profile_router.message(F.text == "/perfil")
async def mostrar_menu_usuario(msg: types.Message):
    users = read_json(USERS_FILE)
    is_user = any(u["user_id"] == msg.from_user.id for u in users.values())

    if not is_user:
        return await msg.reply("🚫 No estás registrado como cliente aún.")

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✏️ Cambiar Prompt"), KeyboardButton(text="🔐 Cambiar API Key")],
            [KeyboardButton(text="⬅️ Cerrar menú")]
        ],
        resize_keyboard=True
    )
    await msg.answer("⚙️ Opciones de perfil:", reply_markup=kb)

# Capturar nuevo prompt
@profile_router.message(F.text == "✏️ Cambiar Prompt")
async def solicitar_prompt(msg: types.Message):
    await msg.answer("✏️ Escribe ahora tu nuevo prompt personalizado.\nEjemplo:\n<i>Responde como un asesor profesional con lenguaje cercano.</i>", 
                     parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

@profile_router.message(F.text.regexp(r"^(Responde|Eres|Actúa)"))
async def guardar_prompt(msg: types.Message):
    users = read_json(USERS_FILE)
    for bc_id, data in users.items():
        if data["user_id"] == msg.from_user.id:
            data["prompt"] = msg.text.strip()
            write_json(USERS_FILE, users)
            return await msg.reply("✅ Prompt actualizado correctamente.\nTu cuenta responderá con esa personalidad.")
    await msg.reply("❌ No encontré tu perfil registrado.")

# Capturar nueva API key
@profile_router.message(F.text == "🔐 Cambiar API Key")
async def solicitar_apikey(msg: types.Message):
    await msg.answer("🔐 Escribe ahora tu nueva clave de OpenAI (formato: sk-xxxxx)", reply_markup=ReplyKeyboardRemove())

@profile_router.message(F.text.regexp(r"^sk-"))
async def guardar_apikey(msg: types.Message):
    users = read_json(USERS_FILE)
    for bc_id, data in users.items():
        if data["user_id"] == msg.from_user.id:
            data["openai_key"] = msg.text.strip()
            write_json(USERS_FILE, users)
            return await msg.reply("✅ API Key guardada correctamente. Tu bot ya está listo para responder.")
    await msg.reply("❌ No encontré tu perfil registrado.")

# Cerrar menú visual
@profile_router.message(F.text == "⬅️ Cerrar menú")
async def cerrar_menu(msg: types.Message):
    await msg.answer("✅ Menú cerrado.", reply_markup=ReplyKeyboardRemove())
