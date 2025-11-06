import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

#--------------------------------------------
#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8517264260:AAE-sPOsWZuYhNxxbxJPh9Rq1laYdjk5HPo")
APP_ID = int(os.environ.get("APP_ID", "27891965")) #Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "909e944f30752b2c47804cbccb8c5c4f") #Your API Hash from my.telegram.org
#--------------------------------------------
OWNER_ID = int(os.environ.get("OWNER_ID", "6146353175")) # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8080")
#--------------------------------------------
DB_URI = os.environ.get("DATABASE_URL","mongodb+srv://thaimozhi2005_db_user:kQiZM67AIF2pOwl5@uptimerobot.s9rgh6m.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", 'UptimeRobot')
#--------------------------------------------
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
#--------------------------------------------

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

#===================(END)========================#

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   
