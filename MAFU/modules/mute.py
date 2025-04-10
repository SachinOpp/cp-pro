from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from functools import wraps
from MAFU import MAFU as app
from config import OTHER_LOGS

FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True,
    can_pin_messages=False
)

MUTE_PERMISSIONS = ChatPermissions()

def mention(user_id, name):
    return f"[{name}](tg://user?id={user_id})"

# Decorator to check if command user is admin
def is_admins(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            user = await client.get_chat_member(message.chat.id, message.from_user.id)
            if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                return await message.reply_text("❌ You need to be an admin to use this command.")
        except:
            return await message.reply_text("⚠️ Failed to check admin status.")
        return await func(client, message, *args, **kwargs)
    return wrapper

# Check if target user is admin
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

# Check if user is already muted
async def is_muted(client, chat_id, user_id):
    try:
        perms = (await client.get_chat_member(chat_id, user_id)).privileges
        return perms is None or not perms.can_send_messages
    except:
        return False

# Extract user and reason
async def extract_user_and_reason(message, client):
    user_id = None
    first_name = None
    reason = None

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        user_id = user.id
        first_name = user.first_name
        reason = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    elif len(message.command) >= 2:
        user_identifier = message.command[1]
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else None

        try:
            user = await client.get_users(user_identifier)
            user_id = user.id
            first_name = user.first_name
        except Exception:
            await message.reply_text(f"⚠️ Cannot find user: `{user_identifier}`")
            return None, None, None
    else:
        await message.reply_text("⚠️ Please reply to a user or use /mute @username.")
        return None, None, None

    return user_id, first_name, reason

# MUTE COMMAND
@app.on_message(filters.command("mute"))
@is_admins
async def mute_command(client, message):
    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    if await is_admin(client, message.chat.id, user_id):
        return await message.reply("⚠️ You cannot mute an admin!")

    if await is_muted(client, message.chat.id, user_id):
        return await message.reply(f"⚠️ {mention(user_id, first_name)} is already muted!")

    try:
        await client.restrict_chat_member(message.chat.id, user_id, MUTE_PERMISSIONS)

        text = (
            f"**User muted successfully.**\n"
            f"**By:** {mention(message.from_user.id, message.from_user.first_name)}\n"
            f"**User:** {mention(user_id, first_name)}"
        )
        if reason:
            text += f"\n**Reason:** `{reason}`"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        await message.reply_text(text, reply_markup=keyboard)

        log_msg = (
            f"**Mute Notification**\n\n"
            f"**Muted By:** {mention(message.from_user.id, message.from_user.first_name)}\n"
            f"**User:** {mention(user_id, first_name)}\n"
            f"**User ID:** `{user_id}`\n"
            f"**Chat:** `{message.chat.title}`\n"
            f"**Chat ID:** `{message.chat.id}`"
        )
        if reason:
            log_msg += f"\n**Reason:** `{reason}`"

        await client.send_message(OTHER_LOGS, log_msg)

    except ChatAdminRequired:
        await message.reply("❌ I don't have permission to mute users!")

# UNMUTE COMMAND
@app.on_message(filters.command("unmute"))
@is_admins
async def unmute_command(client, message):
    user_id, first_name, _ = await extract_user_and_reason(message, client)
    if not user_id:
        return

    if not await is_muted(client, message.chat.id, user_id):
        return await message.reply(f"⚠️ {mention(user_id, first_name)} is not muted!")

    try:
        await client.restrict_chat_member(message.chat.id, user_id, FULL_PERMISSIONS)
        await message.reply(
            f"{mention(user_id, first_name)} has been unmuted.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        log_msg = (
            f"**Unmute Notification (Command)**\n\n"
            f"**Unmuted By:** {mention(message.from_user.id, message.from_user.first_name)}\n"
            f"**User:** {mention(user_id, first_name)}\n"
            f"**User ID:** `{user_id}`\n"
            f"**Chat:** `{message.chat.title}`\n"
            f"**Chat ID:** `{message.chat.id}`"
        )
        await client.send_message(OTHER_LOGS, log_msg)

    except ChatAdminRequired:
        await message.reply("❌ I don't have permission to unmute users!")

# UNMUTE BUTTON HANDLER
@app.on_callback_query(filters.regex(r"^unmute_(\d+)$"))
async def unmute_button(client, callback_query):
    try:
        user = await client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await callback_query.answer("❌ You must be an admin!", show_alert=True)
    except:
        return await callback_query.answer("⚠️ Failed to check admin status.", show_alert=True)

    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id

    if not await is_muted(client, chat_id, user_id):
        return await callback_query.answer("⚠️ Already unmuted!", show_alert=True)

    try:
        await client.restrict_chat_member(chat_id, user_id, FULL_PERMISSIONS)
        await callback_query.message.edit_text(
            f"{mention(user_id, 'User')} has been unmuted.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        user = await client.get_users(user_id)
        log_msg = (
            f"**Unmute Notification (Button)**\n\n"
            f"**Unmuted By:** {mention(callback_query.from_user.id, callback_query.from_user.first_name)}\n"
            f"**User:** {mention(user_id, user.first_name)}\n"
            f"**User ID:** `{user_id}`\n"
            f"**Chat:** `{callback_query.message.chat.title}`\n"
            f"**Chat ID:** `{chat_id}`"
        )
        await client.send_message(OTHER_LOGS, log_msg)

    except:
        await callback_query.answer("❌ Failed to unmute!", show_alert=True)

# CLOSE BUTTON HANDLER
@app.on_callback_query(filters.regex("close"))
async def close_button(client, callback_query):
    await callback_query.message.delete()
