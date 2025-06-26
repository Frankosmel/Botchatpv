from aiogram import Router, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from datetime import datetime, timedelta
from json_utils import read_json, write_json
from config import ADMINS

payment_router = Router()
USERS_FILE = "users.json"

# /planes muestra métodos de pago
@payment_router.message(F.text == "/planes")
async def mostrar_planes(msg: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 Pagar con PayPal")],
            [KeyboardButton(text="💵 Pagar en CUP (Transferencia)")]
        ],
        resize_keyboard=True
    )
    texto = (
        "💼 <b>Planes disponibles:</b>\n\n"
        "🪙 <b>Básico</b>: 7 días – 3 USD / 350 CUP\n"
        "💼 <b>Pro</b>: 30 días – 10 USD / 900 CUP\n\n"
        "📌 Elige un método de pago:"
    )
    await msg.answer(texto, reply_markup=kb, parse_mode="HTML")

# 💳 PayPal
@payment_router.message(F.text == "💳 Pagar con PayPal")
async def pagar_paypal(msg: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Enviar captura de pago")],
            [KeyboardButton(text="⬅️ Volver al menú de pagos")]
        ],
        resize_keyboard=True
    )
    texto = (
        "🔗 Realiza tu pago por PayPal con este botón:\n\n"
        "<a href='https://www.paypal.me/Franchoshop'>🔘 Pagar ahora por PayPal</a>\n\n"
        "💬 Luego envía una captura del pago aquí o por WhatsApp: <b>56246700</b> ✅"
    )
    await msg.answer(texto, parse_mode="HTML", reply_markup=kb, disable_web_page_preview=True)

# 💵 CUP
@payment_router.message(F.text == "💵 Pagar en CUP (Transferencia)")
async def pagar_cup(msg: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Enviar captura de pago")],
            [KeyboardButton(text="⬅️ Volver al menú de pagos")]
        ],
        resize_keyboard=True
    )
    texto = (
        "🏦 <b>Datos para transferencia en CUP:</b>\n\n"
        "💳 <code>9204 1299 7691 8161</code>\n"
        "📞 Número de confirmación obligatorio: <b>56246700</b> ✅\n\n"
        "Una vez realizado el pago, envía la captura aquí o por WhatsApp."
    )
    await msg.answer(texto, parse_mode="HTML", reply_markup=kb)

# 📤 Enviar captura (paso intermedio)
@payment_router.message(F.text == "📤 Enviar captura de pago")
async def capturar_pago(msg: types.Message):
    await msg.answer(
        "📸 Envía ahora la captura del pago realizada.\n"
        "Un administrador revisará tu comprobante y activará tu plan pronto. ✅",
        reply_markup=ReplyKeyboardRemove()
    )

# 📥 Recibir foto o documento como comprobante
@payment_router.message(F.photo | F.document)
async def capturar_archivo_pago(msg: types.Message):
    await msg.reply(
        "📥 Captura recibida correctamente.\n"
        "📌 El equipo revisará tu pago y activará tu plan en breve. Gracias por tu confianza 🙌"
    )

# 🔓 Activación manual por el admin
@payment_router.message(F.text.regexp(r"^activar bc.+ \d+$"))
async def activar_plan(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.reply("🚫 Solo los administradores pueden usar este comando.")

    try:
        _, bcid, dias = msg.text.split()
        dias = int(dias)
        users = read_json(USERS_FILE)
        if bcid not in users:
            return await msg.reply("❌ ID no encontrado.")

        nueva_fecha = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
        users[bcid]["expires_at"] = nueva_fecha
        write_json(USERS_FILE, users)

        # Notificación al cliente
        try:
            await msg.bot.send_message(
                chat_id=users[bcid]["user_id"],
                text=f"✅ Tu plan fue activado por {dias} días. ¡Gracias por tu pago! 💼"
            )
        except:
            pass

        await msg.reply(f"🟢 Activado hasta {nueva_fecha} para @{users[bcid]['username']}.")
    except:
        await msg.reply("❌ Formato inválido. Usa: activar bc123 30")
