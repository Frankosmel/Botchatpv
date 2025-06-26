from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from json_utils import read_json, write_json
from aiogram import Bot

USERS_FILE = "users.json"

def start_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_expired_clients, "interval", hours=1, args=[bot])
    scheduler.start()

async def check_expired_clients(bot: Bot):
    users = read_json(USERS_FILE)
    today = datetime.now().date()
    changed = False

    for bc_id, data in list(users.items()):
        expires = data.get("expires_at")
        if expires and datetime.strptime(expires, "%Y-%m-%d").date() < today:
            try:
                await bot.send_message(
                    chat_id=data["user_id"],
                    text="⏰ Tu plan ha expirado. Si deseas renovarlo, contáctanos nuevamente."
                )
                # Cerrar la conexión Business (Bot API lo permite desde versión 7.0)
                await bot.close_business_connection(bc_id)
            except:
                pass  # Por si ya no se puede notificar

            users.pop(bc_id)
            changed = True

    if changed:
        write_json(USERS_FILE, users)
