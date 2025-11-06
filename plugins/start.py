import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from database.database import *
from helper_func import *

START_MSG = """<b>◈ ʜᴇʏ!!

<blockquote>ʟᴏᴠᴇ ᴀɴɪᴍᴇ? ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ.</blockquote></b>
        
<b>›› /add_admin :</b> Add an Admin
<b>›› /deladmin :</b> Remove an Admin
<b>›› /admins :</b> Get Admin List
<b>›› /spoiler :</b> Make Spoiler Image
<b>›› /stats :</b> View Run Time

"""

# Commands for admins and owner
@Client.on_message(filters.command('start') & filters.private & admin)
async def start_command(client: Client, message: Message):
    await message.delete()
    await message.reply_text(
        text = START_MSG.format(),
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]]),
        message_effect_id=5104841245755180586 # 🔥
    )
    await asyncio.sleep(600)

# ================================================================================================= #

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
