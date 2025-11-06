import asyncio
import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from database.database import db

logger = logging.getLogger(__name__)

# ----------------- ADMIN FILTER -----------------
def admin_filter(_, __, message: Message):
    return message.from_user.id == OWNER_ID or message.from_user.id in asyncio.run(db.get_all_admins())

admin_only = filters.create(admin_filter)

# ----------------- ADD BOT COMMAND -----------------
@Client.on_message(filters.command("addbot") & admin_only & filters.private)
async def add_bot_command(client: Client, message: Message):
    """
    Add a bot to uptime monitoring
    """
    try:
        await message.reply_text(
            "📝 <b>Add Bot to Uptime Monitoring</b>\n\n"
            "Please send the bot username (without @)\n"
            "Example: <code>MyAwesomeBot</code>",
            quote=True
        )

        username_msg = await client.listen(message.chat.id, filters=filters.text, timeout=60)
        bot_username = username_msg.text.strip().replace("@", "")

        await username_msg.reply_text(
            f"✅ Bot Username: <code>@{bot_username}</code>\n\n"
            "Now send the webhook URL\n"
            "Example: <code>https://yourbot.onrender.com/</code>"
        )

        webhook_msg = await client.listen(message.chat.id, filters=filters.text, timeout=60)
        webhook_url = webhook_msg.text.strip()

        if not webhook_url.startswith(("http://", "https://")):
            return await webhook_msg.reply_text("❌ Invalid URL! Must start with http:// or https://")

        await webhook_msg.reply_text(
            f"✅ Webhook: <code>{webhook_url}</code>\n\n"
            "Now send the ping interval in seconds.\n"
            "Example: <code>300</code> (5 minutes)"
        )

        interval_msg = await client.listen(message.chat.id, filters=filters.text, timeout=60)
        try:
            interval = int(interval_msg.text.strip())
            if interval < 60:
                return await interval_msg.reply_text("❌ Interval must be at least 60 seconds!")
        except ValueError:
            return await interval_msg.reply_text("❌ Invalid number! Please send a number in seconds.")

        await db.add_bot_for_uptime(bot_username, webhook_url, interval, message.from_user.id)

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
        await interval_msg.reply_text(
            "✅ <b>Bot Added Successfully!</b>\n\n"
            f"<b>Username:</b> @{bot_username}\n"
            f"<b>Webhook:</b> <code>{webhook_url}</code>\n"
            f"<b>Interval:</b> {interval} seconds\n\n"
            "🔄 Monitoring will start automatically.",
            reply_markup=reply_markup
        )

    except asyncio.TimeoutError:
        await message.reply_text("⏱️ Timeout! Please try again using /addbot")
    except Exception as e:
        logger.error(f"Error in /addbot: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


# ----------------- REMOVE BOT COMMAND -----------------
@Client.on_message(filters.command("removebot") & admin_only & filters.private)
async def remove_bot_command(client: Client, message: Message):
    try:
        bot = await db.get_uptime_bot()
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

        if not bot:
            return await message.reply_text("❌ No bot currently monitored.", reply_markup=reply_markup)

        await message.reply_text(
            f"⚠️ Confirm Removal\n\n"
            f"Bot: @{bot['username']}\n"
            f"Webhook: <code>{bot['webhook']}</code>\n\n"
            f"Send <b>YES</b> to confirm removal or <b>NO</b> to cancel.",
            quote=True
        )

        confirm_msg = await client.listen(message.chat.id, filters=filters.text, timeout=30)
        if confirm_msg.text.strip().upper() == "YES":
            await db.remove_uptime_bot()
            await confirm_msg.reply_text("✅ Bot removed from monitoring.", reply_markup=reply_markup)
        else:
            await confirm_msg.reply_text("❌ Cancelled.", reply_markup=reply_markup)

    except asyncio.TimeoutError:
        await message.reply_text("⏱️ Timeout! Removal cancelled.")
    except Exception as e:
        logger.error(f"Error in /removebot: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


# ----------------- STATUS COMMAND -----------------
@Client.on_message(filters.command("status") & admin_only & filters.private)
async def status_command(client: Client, message: Message):
    try:
        bot = await db.get_uptime_bot()
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

        if not bot:
            return await message.reply_text(
                "❌ No bot configured.\nUse /addbot to add one.",
                reply_markup=reply_markup
            )

        # Status text
        if bot['is_online'] is None:
            emoji, text = "❓", "Not checked yet"
        elif bot['is_online']:
            emoji, text = "✅", "Online"
        else:
            emoji, text = "❌", "Offline"

        last_check = (
            bot['last_checked'].strftime("%d-%b-%Y %I:%M:%S %p")
            if bot['last_checked']
            else "Never"
        )

        msg = (
            f"🤖 <b>Bot Uptime Status</b>\n\n"
            f"<b>Bot:</b> @{bot['username']}\n"
            f"<b>Status:</b> {emoji} {text}\n"
            f"<b>Webhook:</b> <code>{bot['webhook']}</code>\n"
            f"<b>Interval:</b> {bot['interval']} sec\n"
            f"<b>Last Checked:</b> {last_check}\n"
            f"<b>Message:</b> {bot.get('status_msg', 'N/A')}"
        )

        await message.reply_text(msg, reply_markup=reply_markup)

    except Exception as e:
        logger.error(f"Error in /status: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


# ----------------- HELP COMMAND -----------------
@Client.on_message(filters.command("uptimehelp") & admin_only & filters.private)
async def uptime_help_command(client: Client, message: Message):
    help_text = (
        "🧠 <b>Uptime Monitor Commands</b>\n\n"
        "<b>/addbot</b> - Add a bot to uptime monitoring\n"
        "<b>/removebot</b> - Remove monitored bot\n"
        "<b>/status</b> - Check uptime status\n"
        "<b>/uptimehelp</b> - Show this help\n\n"
        "⚙️ Bot automatically pings your webhook periodically to stay alive."
    )
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    await message.reply_text(help_text, reply_markup=reply_markup)


# ----------------- NON-ADMIN HANDLER -----------------
@Client.on_message(filters.command(["addbot", "removebot", "status", "uptimehelp"]) & ~admin_only & filters.private)
async def non_admin_handler(client: Client, message: Message):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    await message.reply_text(
        "⛔ <b>Access Denied</b>\n\nOnly admins can use uptime commands.",
        reply_markup=reply_markup
    )

