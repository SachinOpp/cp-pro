import re
import asyncio
from pyrogram import Client, filters, enums, errors
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from MAFU import MAFU as app
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, OTHER_LOGS, BOT_USERNAME

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["BioFilterBot"]
bio_filter_collection = db["bio_filter"]

url_pattern = re.compile(r"(https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/[a-zA-Z0-9._%+-]*)?")
username_pattern = re.compile(r"@[\w]+")

async def is_admins(client, chat_id, user_id):
    try:
        async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if member.user.id == user_id:
                return True
        return False
    except Exception as e:
        print(f"[is_admin ERROR] {e}")
        return False

@app.on_message(filters.group)
async def check_bio(client, message):
    if message.text and message.text.startswith("/"):
        return  # Ignore commands

    chat_id = message.chat.id
    user = message.from_user

    if not user or await is_admins(client, chat_id, user.id):
        return

    try:
        user_full = await client.get_chat(user.id)
        bio = user_full.bio
    except Exception as e:
        print(f"[get_chat ERROR] {e}")
        return

    if not bio:
        return

    if re.search(url_pattern, bio) or re.search(username_pattern, bio):
        try:
            await message.delete()
        except errors.MessageDeleteForbidden:
            return

        mention = f"[{user.first_name}](tg://user?id={user.id})"
        username = f"@{user.username}" if user.username else "No username"
        group_name = message.chat.title

        log_text = f"""
**Bio Filter Log**

**Full Name:** {user_full.first_name} {user_full.last_name or ''}
**Username:** {username}
**User ID:** `{user.id}`
**Mention:** {mention}
**Group Name:** `{group_name}`
**Group Chat ID:** `{chat_id}`
**User Bio:** `{bio}`
**User Message:** `{message.text or 'Media Message'}`

**Bot Name:** @{BOT_USERNAME}
"""

        try:
            await client.send_message(
                OTHER_LOGS,
                log_text,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("➕ Add me in your group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]]
                )
            )
        except Exception as e:
            print(f"[LOG ERROR] {e}")

        try:
            warn_msg = await message.reply_text(
                f"{mention}, please remove link or username from your bio!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]),
                parse_mode=enums.ParseMode.MARKDOWN
            )
            await asyncio.sleep(10)
            await warn_msg.delete()
        except Exception as e:
            print(f"[WARN MSG ERROR] {e}")
