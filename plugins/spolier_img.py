import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from database.database import *
from helper_func import *

# Spoiler command for owner
@Client.on_message(filters.command('spoiler') & filters.private & admin)
async def spoiler_command(client: Client, message: Message):
    """Handle /spoiler command"""
    if not message.reply_to_message:
        await message.reply_text(
            "🎭 Spoiler Feature\n\n"
            "How to use:\n"
            "1. Someone sends a photo\n"
            "2. Reply to it with /spoiler\n"
            "3. Bot resends as blurred/hidden image\n"
            "4. Click to reveal!\n\n"
            "Try it: Reply to any photo with /spoiler"
        )
        return
    
    replied_message = message.reply_to_message
    
    if replied_message.photo:
        try:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=replied_message.photo.file_id,
                caption=replied_message.caption,
                has_spoiler=True
            )
            await message.reply_text(
                "✅ Spoiler sent!\n\n"
                "👆 Click the blurred image to reveal it.\n"
                "🎭 Perfect for hiding spoilers!"
            )
        except Exception as e:
            await message.reply_text(f"❌ Failed to send spoiler: `{str(e)}`")
    
    elif replied_message.document:
        mime_type = replied_message.document.mime_type or ""
        if mime_type.startswith('image/'):
            try:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=replied_message.document.file_id,
                    caption=replied_message.caption,
                    has_spoiler=True
                )
                await message.reply_text("✅ **Spoiler sent!**\n\n👆 Click the blurred image to reveal it.")
            except Exception as e:
                await message.reply_text(f"❌ Failed: `{str(e)}`")
        else:
            await message.reply_text(
                f"❌ This is not an image file.\n\n"
                f"File type: `{mime_type}`\n"
                f"Please reply to a photo or image document."
            )
    else:
        await message.reply_text(
            "❌ Invalid target!\n\n"
            "Please reply to:\n"
            "✅ A photo\n"
            "✅ An image document\n\n"
            "Current message type is not supported."
        )
