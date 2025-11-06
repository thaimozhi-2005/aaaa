import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables (for local dev or Render)
load_dotenv()

# ==================================================
# 🔐 Telegram API Credentials (from @BotFather & my.telegram.org)
# ==================================================
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")  # required
APP_ID = int(os.environ.get("APP_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

# ==================================================
# 👑 Bot Owner & Workers
# ==================================================
OWNER_ID = int(os.environ.get("OWNER_ID", 0))  # your Telegram ID
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))

# ==================================================
# 🌐 MongoDB Database Connection
# ==================================================
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "UptimeRobot")

# ==================================================
# 🌍 Web Server (Render uses PORT automatically)
# ==================================================
PORT = int(os.environ.get("PORT", "8080"))

# ==================================================
# 🧠 Bot Texts
# ==================================================
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

# ==================================================
# 🪵 Logging Configuration
# ==================================================
LOG_FILE_NAME = "filesharingbot.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
