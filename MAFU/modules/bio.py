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

async def get_bio_filter_status(chat_id):
    data = await bio_filter_collection.find_one({"chat_id": chat_id})
    return data["enabled"] if data else False

async def is_admins(client, chat_id, user_id):
    try:
        async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if member.user.id == user_id:
                return True
        return False
    except Exception as e:
        print(f"[is_admin ERROR] {e}")
        return False

@app.on_message(filters.command("biobot") & filters.group)
async def toggle_bio_filter(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admins(client, chat_id, user_id):
        await message.reply_text("You must be an admin to use this command!")
        return

    buttons = [
        [InlineKeyboardButton("Enable Bio Filter ✅", callback_data=f"enable_bio_{chat_id}")],
        [InlineKeyboardButton("Disable Bio Filter ❌", callback_data=f"disable_bio_{chat_id}")],
    ]

    await message.reply_text(
        "Choose an option to enable or disable the Bio Filter:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id

    if data.startswith("enable_bio_"):
        if not await is_admins(client, chat_id, user_id):
            await callback_query.answer("You are not an administrator!", show_alert=True)
            return

        await bio_filter_collection.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
        await callback_query.message.edit_text("Bio Filter has been enabled! ✅")
        await callback_query.answer("Bio filter enabled successfully!")

    elif data.startswith("disable_bio_"):
        if not await is_admins(client, chat_id, user_id):
            await callback_query.answer("You are not an administrator!", show_alert=True)
            return

        await bio_filter_collection.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
        await callback_query.message.edit_text("Bio Filter has been disabled! ❌")
        await callback_query.answer("Bio filter disabled successfully!")

@app.on_message(filters.group)
async def check_bio(client, message):
    chat_id = message.chat.id
    user = message.from_user

    if not user or await is_admins(client, chat_id, user.id):
        return

    if not await get_bio_filter_status(chat_id):
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
            await client.send_message(OTHER_LOGS, log_text)
        except Exception as e:
            print(f"[LOG ERROR] {e}")

        try:
            warn_msg = await message.reply_text(
                f"{mention}, please remove link or username from your bio!\n\nCommand to control: /biobot",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            await asyncio.sleep(10)
            await warn_msg.delete()
        except Exception as e:
            print(f"[WARN MSG ERROR] {e}")
