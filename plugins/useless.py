import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from helper_func import *

#=====================================================================================##

# stats command

@Client.on_message(filters.command('stats') & filters.private & admin)
async def stats(bot: Client, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.delete()
    await message.reply(BOT_STATS_TEXT.format(uptime=time))
    await asyncio.sleep(180)
