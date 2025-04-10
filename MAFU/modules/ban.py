from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from functools import wraps

from MAFU import MAFU as app  # Replace with your Client name
from config import OTHER_LOGS  # Logger Chat ID

# Mention Function
def mention(user_id, name):
    return f"[{name}](tg://user?id={user_id})"

# Admin Check Decorator
def is_admins(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            user = await client.get_chat_member(message.chat.id, message.from_user.id)
            if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                return await message.reply_text("You need to be an admin to use this command.")
        except Exception as e:
            return await message.reply_text("Failed to check admin status.")
        return await func(client, message, *args, **kwargs)
    return wrapper

# Extract User & Reason
async def extract_user_and_reason(message, client):
    args = message.text.split(maxsplit=2)
    user = None
    reason = None

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(args) > 1:
            reason = args[1]
    elif len(args) > 1:
        user_arg = args[1]
        reason = args[2] if len(args) > 2 else None
        try:
            user = await client.get_users(user_arg)
        except Exception:
            await message.reply_text("User not found!")
            return None, None, None

    if not user:
        await message.reply_text("Reply to a user or mention one!")
        return None, None, None

    try:
        member = await client.get_chat_member(message.chat.id, user.id)
    except UserNotParticipant:
        pass
    else:
        if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await message.reply_text("You can't ban an admin!")
            return None, None, None

    return user.id, user.first_name, reason

# Ban Command
@app.on_message(filters.command("ban", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
@is_admins
async def ban_user(client, message):
    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.ban_chat_member(message.chat.id, user_id)
        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        msg = f"**User Banned Successfully!**\n\n**Banned By:** {admin_mention}\n**User:** {user_mention}"
        if reason:
            msg += f"\n**Reason:** `{reason}`"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Unban", callback_data=f"unban_{user_id}")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])

        await message.reply_text(msg, reply_markup=keyboard, disable_web_page_preview=True)

        # Send log to OTHER_LOGS
        log_msg = f"**Ban Alert**\n\n**Chat:** {message.chat.title} (`{message.chat.id}`)\n**By:** {admin_mention}\n**User:** {user_mention}"
        if reason:
            log_msg += f"\n**Reason:** `{reason}`"
        await client.send_message(OTHER_LOGS, log_msg)

    except ChatAdminRequired:
        await message.reply_text("I need admin rights to ban users.")

# Unban Command
@app.on_message(filters.command("unban", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
@is_admins
async def unban_user(client, message):
    user_id, first_name, _ = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"{mention(user_id, first_name)} has been unbanned!",
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))

        # Send log to OTHER_LOGS
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        user_mention = mention(user_id, first_name)
        log_msg = f"**Unban Alert**\n\n**Chat:** {message.chat.title} (`{message.chat.id}`)\n**By:** {admin_mention}\n**User:** {user_mention}"
        await client.send_message(OTHER_LOGS, log_msg)

    except ChatAdminRequired:
        await message.reply_text("I need admin rights to unban users.")

# Unban Button Callback
@app.on_callback_query(filters.regex(r"^unban_(\d+)$"))
async def unban_btn_callback(client, cb):
    user_id = int(cb.data.split("_")[1])
    chat_id = cb.message.chat.id
    admin = cb.from_user

    member = await client.get_chat_member(chat_id, admin.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await cb.answer("You're not an admin!", show_alert=True)

    try:
        await client.unban_chat_member(chat_id, user_id)
        await cb.message.edit_text(
            "User unbanned successfully!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        # Send log to OTHER_LOGS
        user = await client.get_users(user_id)
        admin_mention = mention(admin.id, admin.first_name)
        user_mention = mention(user_id, user.first_name)
        log_msg = f"**Unban (Button) Alert**\n\n**Chat:** {cb.message.chat.title} (`{chat_id}`)\n**By:** {admin_mention}\n**User:** {user_mention}"
        await client.send_message(OTHER_LOGS, log_msg)

    except Exception:
        await cb.answer("Failed to unban the user.", show_alert=True)
