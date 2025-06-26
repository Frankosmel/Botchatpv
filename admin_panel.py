from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import ADMINS
from json_utils import read_json, write_json
from datetime import datetime, timedelta

admin_router = Router()
USERS_FILE = "users.json"

@admin_router.message(F.text == "/admin")
async def show_admin_panel(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.reply("🚫 No tienes permiso para acceder al panel.")

    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📋 Ver clientes activos")],
        [KeyboardButton(text="🕓 Cambiar vencimiento")],
        [KeyboardButton(text="🔑 Cambiar API key"), KeyboardButton(text="🧠 Cambiar prompt")],
        [KeyboardButton(text="❌ Eliminar cliente")],
        [KeyboardButton(text="⬅️ Volver")]
    ], resize_keyboard=True)

    await msg.answer("⚙️ Panel de Administración:", reply_markup=kb)

@admin_router.message(F.text == "📋 Ver clientes activos")
async def listar_clientes(msg: types.Message):
    users = read_json(USERS_FILE)
    if not users:
        return await msg.reply("⚠️ No hay usuarios registrados.")

    texto = "📋 <b>Clientes conectados:</b>\n\n"
    for bc_id, data in users.items():
        username = data.get("username", "Desconocido")
        expires = data.get("expires_at", "∞")
        texto += f"👤 <b>@{username}</b>\n🆔 <code>{bc_id}</code>\n⏰ Plan hasta: <b>{expires}</b>\n\n"

    await msg.reply(texto, parse_mode=ParseMode.HTML)

@admin_router.message(F.text == "🕓 Cambiar vencimiento")
async def cambiar_vencimiento(msg: types.Message):
    await msg.answer("✏️ Escribe el ID del cliente y nueva duración (en días).\nEjemplo: `bc123 30`", reply_markup=ReplyKeyboardRemove())

@admin_router.message(F.text.regexp(r"^bc.+ \d+$"))
async def aplicar_vencimiento(msg: types.Message):
    bcid, dias = msg.text.split()
    users = read_json(USERS_FILE)
    if bcid not in users:
        return await msg.reply("❌ ID no encontrado.")

    nueva_fecha = (datetime.now() + timedelta(days=int(dias))).strftime("%Y-%m-%d")
    users[bcid]["expires_at"] = nueva_fecha
    write_json(USERS_FILE, users)
    await msg.reply(f"✅ Fecha de vencimiento actualizada a: {nueva_fecha}")

@admin_router.message(F.text == "🔑 Cambiar API key")
async def pedir_apikey(msg: types.Message):
    await msg.answer("✏️ Envía el ID del cliente seguido de la nueva API key.\nEjemplo:\n`bc123 sk-xxxxx`", reply_markup=ReplyKeyboardRemove())

@admin_router.message(F.text.regexp(r"^bc.+ sk-"))
async def aplicar_apikey(msg: types.Message):
    bcid, apikey = msg.text.split()
    users = read_json(USERS_FILE)
    if bcid not in users:
        return await msg.reply("❌ ID no encontrado.")
    users[bcid]["openai_key"] = apikey
    write_json(USERS_FILE, users)
    await msg.reply("✅ API key actualizada correctamente.")

@admin_router.message(F.text == "🧠 Cambiar prompt")
async def pedir_prompt(msg: types.Message):
    await msg.answer("✏️ Envía el ID del cliente seguido del nuevo prompt.\nEjemplo:\n`bc123 Responde como doctor.`", reply_markup=ReplyKeyboardRemove())

@admin_router.message(F.text.regexp(r"^bc.+ "))
async def aplicar_prompt(msg: types.Message):
    try:
        bcid, *nuevo_prompt = msg.text.split()
        nuevo_prompt = " ".join(nuevo_prompt)
        users = read_json(USERS_FILE)
        if bcid not in users:
            return await msg.reply("❌ ID no encontrado.")
        users[bcid]["prompt"] = nuevo_prompt
        write_json(USERS_FILE, users)
        await msg.reply("✅ Prompt actualizado correctamente.")
    except:
        await msg.reply("❌ Formato inválido.")

@admin_router.message(F.text == "❌ Eliminar cliente")
async def eliminar_cliente(msg: types.Message):
    await msg.answer("✏️ Escribe el ID del cliente que deseas eliminar (ej: bc123):", reply_markup=ReplyKeyboardRemove())

@admin_router.message(F.text.regexp(r"^bc.+"))
async def confirmar_eliminacion(msg: types.Message):
    bcid = msg.text.strip()
    users = read_json(USERS_FILE)
    if bcid in users:
        users.pop(bcid)
        write_json(USERS_FILE, users)
        await msg.reply("✅ Cliente eliminado correctamente.")
    else:
        await msg.reply("❌ ID no encontrado.")

@admin_router.message(F.text == "⬅️ Volver")
async def volver_menu(msg: types.Message):
    await show_admin_panel(msg)
