from json_utils import read_json

CONFIG = read_json("config.json")

BOT_TOKEN = CONFIG["bot_token"]
ADMINS = CONFIG["admins"]
