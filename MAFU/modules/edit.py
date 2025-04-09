from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from pymongo import MongoClient

from MAFU import MAFU as app
from config import MONGO_URL, OTHER_LOGS, BOT_USERNAME
from MAFU.helper.auth import is_auth
from MAFU.helper.admin import is_admins

# Mongo Setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["copyright"]
settings_col = db["EditDeleteSettings"]

# Get current delete setting
def get_delete_status(chat_id):
    setting = settings_col.find_one({"chat_id": chat_id})
    return setting["delete_enabled"] if setting else True

# Set delete status
def set_delete_status(chat_id, status):
    settings_col.update_one({"chat_id": chat_id}, {"$set": {"delete_enabled": status}}, upsert=True)

# Command to toggle the edit delete feature
@app.on_message(filters.command("edit") & filters.group)
async def edit_toggle(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admins(chat_id, user_id):
        return await message.reply_text(
            "You are not an admin!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

    try:
        bot_member = await client.get_chat_member(chat_id, client.me.id)
        if not bot_member.privileges or not bot_member.privileges.can_delete_messages:
            return await message.reply(
                f"{message.from_user.mention}, I don't have delete permission!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
            )
    except:
        return

    status = "ON" if get_delete_status(chat_id) else "OFF"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ON", callback_data="edit_on"),
         InlineKeyboardButton("OFF", callback_data="edit_off")],
        [InlineKeyboardButton("Close", callback_data="close")]
    ])
    await message.reply(f"Edit delete feature is currently {status}.", reply_markup=keyboard)

# Handle button actions
@app.on_callback_query(filters.regex("^edit_"))
async def handle_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    data = callback_query.data

    if not await is_admins(chat_id, user_id):
        return await callback_query.answer("You are not authorized!", show_alert=True)

    if data == "edit_on":
        set_delete_status(chat_id, True)
        await callback_query.message.edit_text("Edit delete feature is now ON.")
    elif data == "edit_off":
        set_delete_status(chat_id, False)
        await callback_query.message.edit_text("Edit delete feature is now OFF.")
    elif data == "edit_close":
        try:
            await callback_query.message.delete()
        except:
            pass

# Delete edited message if not admin/auth
@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_message(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if await is_admins(chat_id, user_id):
        return
    if await is_auth(chat_id, user_id):
        return
    if not get_delete_status(chat_id):
        return

    try:
        bot_member = await client.get_chat_member(chat_id, client.me.id)
        if not bot_member.privileges or not bot_member.privileges.can_delete_messages:
            return

        old_text = message.text or "No text available"
        await asyncio.sleep(2)
        await message.delete()

        # Log text for OTHER_LOGS
        log_text = (
            f"Edited message deleted!\n\n"
            f"User: {message.from_user.first_name}"
            f"User id: `{user_id}`\n"
            f"Username: @{message.from_user.username if message.from_user.username else 'None'}\n"
            f"Mention: {message.from_user.mention}\n"
            f"Group: {message.chat.title}\n"
            f"Chat ID: {chat_id}\n"
            f"Edited message: `{message.text}`\n\n"
            f"**Bot Name: @{BOT_USERNAME}**"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add me in your group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
        ])
        await client.send_message(OTHER_LOGS, log_text, reply_markup=keyboard)

        # Notification to user
        user_notice_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("View Your Edit Logs", url="https://t.me/Copyright_logs")]
        ])
        sent_msg = await message.reply(
            f"Hey {message.from_user.mention},\n"
            f"You edited a message, so I deleted it.\n\n"
            f"To turn this feature on|off, use /edit",
            reply_markup=user_notice_keyboard
        )
        await asyncio.sleep(10)
        try:
            await sent_msg.delete()
        except:
            pass

    except Exception as e:
        print(f"[EditDelete Error] {e}")
