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
