from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired
from MAFU import MAFU as app
from config import OTHER_LOGS, BOT_USERNAME
from typing import Tuple, Optional

# =================== EXTRACT UTILS ===================
async def extract_user_and_reason(message: Message, client: Client) -> Tuple[Optional[int], Optional[str], Optional[str]]:
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
            if user_identifier.startswith("@"):
                user = await client.get_users(user_identifier)
            else:
                user = await client.get_users(int(user_identifier))
            user_id = user.id
            first_name = user.first_name
        except Exception:
            await message.reply_text(f"Can't find this user: `{user_identifier}`")
            return None, None, None
    else:
        await message.reply_text("Reply to a user or give a username/userid.")
        return None, None, None

    return user_id, first_name, reason


def mention(user_id: int, name: str) -> str:
    return f"[{name}](tg://user?id={user_id})"

# =================== PERMISSIONS ===================
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

# =================== MUTE COMMAND ===================
@app.on_message(filters.command("mute", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def mute_command_handler(client, message):
    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.restrict_chat_member(message.chat.id, user_id, MUTE_PERMISSIONS)
        user = await client.get_users(user_id)
        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)

        msg = f"**User muted successfully.**\n\n**Muted by:** {admin_mention}\n**User:** {user_mention}"
        if reason:
            msg += f"\n**Reason:** `{reason}`"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        await message.reply_text(msg, reply_markup=keyboard)

        # Logger
        user_username = f"@{user.username}" if user.username else "No username"
        log_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Add me in your group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]])
        log_msg = (
            f"Mute Notification !\n\n"
            f"**Muted by:** {admin_mention}\n"
            f"**User:** {user_mention}\n"
            f"**Username:** `{user_username}`\n"
            f"**User ID:** `{user_id}`\n"
            f"**Chat:** `{message.chat.title}`\n"
            f"**Chat ID:** `{message.chat.id}`"
        )
        if reason:
            log_msg += f"\n**Reason:** `{reason}`"
        await client.send_message(OTHER_LOGS, log_msg, reply_markup=log_keyboard)

    except ChatAdminRequired:
        await message.reply_text(
            "I need to be an admin with mute permissions!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

# =================== UNMUTE BY BUTTON ===================
@app.on_callback_query(filters.regex(r"^unmute_(\d+)$"))
async def unmute_callback(client, callback_query):
    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id
    from_user = callback_query.from_user  

    try:
        await client.restrict_chat_member(chat_id, user_id, FULL_PERMISSIONS)
        await callback_query.message.edit_text(
            "User unmuted successfully.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        user = await client.get_users(user_id)
        user_username = f"@{user.username}" if user.username else "No username"
        log_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Add me in your group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]])
        log_msg = (
            f"Unmute Notification !\n\n"
            f"**Unmuted by:** {mention(from_user.id, from_user.first_name)}\n"
            f"**User:** {mention(user.id, user.first_name)}\n"
            f"**Username:** `{user_username}`\n"
            f"**User ID:** `{user.id}`\n"
            f"**Chat:** `{callback_query.message.chat.title}`\n"
            f"**Chat ID:** `{chat_id}`"
        )
        await client.send_message(OTHER_LOGS, log_msg, reply_markup=log_keyboard)

    except Exception:
        await callback_query.answer("Failed to unmute the user!", show_alert=True)

# =================== UNMUTE BY COMMAND ===================
@app.on_message(filters.command("unmute", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def unmute_user(client, message):
    user_id, first_name, _ = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.restrict_chat_member(message.chat.id, user_id, FULL_PERMISSIONS)
        await message.reply_text(
            f"{mention(user_id, first_name)} has been unmuted successfully.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        user = await client.get_users(user_id)
        user_username = f"@{user.username}" if user.username else "No username"
        log_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Add me in your group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]])
        log_msg = (
            f"Unmute Notification !\n\n"
            f"**Unmuted by:** {mention(message.from_user.id, message.from_user.first_name)}\n"
            f"**User:** {mention(user_id, first_name)}\n"
            f"**Username:** `{user_username}`\n"
            f"**User ID:** `{user_id}`\n"
            f"**Chat:** `{message.chat.title}`\n"
            f"**Chat ID:** `{message.chat.id}`"
        )
        await client.send_message(OTHER_LOGS, log_msg, reply_markup=log_keyboard)

    except ChatAdminRequired:
        await message.reply_text(
            "I need admin privileges to unmute users!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )
