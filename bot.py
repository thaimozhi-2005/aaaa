from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import pytz
from datetime import datetime
from config import *
import logging
import aiohttp
from database.database import db
import importlib
import os
import traceback

# Suppress APScheduler logs below WARNING level
logging.getLogger("apscheduler").setLevel(logging.WARNING)

name = """
 BY SS BOTZ
"""

def get_indian_time():
    """Returns the current time in IST."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)

'''
#def debug_load_plugins():
    """Safely loads all plugins and logs errors."""
    print("\n🧩 Checking plugins in ./plugins folder...\n")
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"plugins.{file[:-3]}"
            try:
                importlib.import_module(module_name)
                print(f"✅ Loaded plugin: {module_name}")
            except Exception as e:
                print(f"❌ Failed to load {module_name}: {e}")
                traceback.print_exc()
    print("\n✅ Plugin check complete.\n")

debug_load_plugins() '''

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER
        self.username = None

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.username = usr_bot_me.username
        self.uptime = datetime.now()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by https://t.me/SSbotz_Support")
        self.LOGGER(__name__).info(
            f"""
 _______ ______   ___  ___ _____ _____ 
/   ___//  ___/  | _ )/ _ \\_   _/ _   /
\\____ \\\\____ \\   | _ \\ (_) || |   / /_
/_____//_____/   |___/\\___/ |_|  /____|
                                                         
                                          """
        )

        # Start background uptime loop
        await self.start_uptime_loop()

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        # Notify owner
        try:
            await self.send_message(OWNER_ID, text=f"<b><blockquote>🚀 Bot Restarted Successfully!</blockquote></b>")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Could not send restart message: {e}")

    """async def start_uptime_loop(self):
        session = aiohttp.ClientSession()

        async def ping_loop():
            while True:
                bot_info = await db.get_uptime_bot()
                if bot_info:
                    try:
                        async with session.get(bot_info["webhook"], timeout=10) as resp:
                            if resp.status == 200:
                                await db.update_uptime_status(bot_info["username"], True, "OK")
                                self.LOGGER(__name__).info(f"[Uptime ✅] {bot_info['username']} is Online.")
                            else:
                                await db.update_uptime_status(bot_info["username"], False, f"HTTP {resp.status}")
                                self.LOGGER(__name__).warning(f"[Uptime ❌] {bot_info['username']} returned HTTP {resp.status}")
                    except Exception as e:
                        await db.update_uptime_status(bot_info["username"], False, str(e))
                        self.LOGGER(__name__).error(f"[Uptime ❌] {bot_info['username']} Error: {e}")
                    await asyncio.sleep(bot_info["interval"])
                else:
                    await asyncio.sleep(300)  # no bot configured, recheck every 5 min

        asyncio.create_task(ping_loop())"""

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        self.LOGGER(__name__).info("Bot is now running. Thanks to @SS_Botz")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())


if __name__ == "__main__":
    Bot().run()

