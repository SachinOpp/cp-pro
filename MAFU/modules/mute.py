from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions
from functools import wraps

from MAFU import MAFU as app  # Your client name
from config import OTHER_LOGS  # Logger Chat ID


# Mention Helper
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
        except Exception:
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
    except Exception:
        pass
    else:
        if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await message.reply_text("You can't mute an admin!")
            return None, None, None

    return user.id, user.first_name, reason


# Mute Command
@app.on_message(filters.command("mute", prefixes=["/", "!", "#", ".", "@", ","]))
@is_admins
async def mute_user(client, message):
    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=ChatPermissions()  # No permissions
        )
        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        msg = f"**User Muted Successfully!**\n\n**Muted By:** {admin_mention}\n**User:** {user_mention}"
        if reason:
            msg += f"\n**Reason:** `{reason}`"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])

        await message.reply_text(msg, reply_markup=keyboard, disable_web_page_preview=True)

        # Log
        log_msg = f"**Mute Alert**\n\n**Chat:** {message.chat.title} (`{message.chat.id}`)\n**By:** {admin_mention}\n**User:** {user_mention}"
        if reason:
            log_msg += f"\n**Reason:** `{reason}`"
        await client.send_message(OTHER_LOGS, log_msg)

    except ChatAdminRequired:
        await message.reply_text("I need admin rights to mute users.")


# Unmute Command
@app.on_message(filters.command("unmute", prefixes=["/", "!", "#", ".", "@", ","]))
@is_admins
async def unmute_user(client, message):
    user_id, first_name, _ = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=enums.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            ),
        )
        await message.reply_text(f"{mention(user_id, first_name)} has been unmuted!",
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))

        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        user_mention = mention(user_id, first_name)
        log_msg = f"**Unmute Alert**\n\n**Chat:** {message.chat.title} (`{message.chat.id}`)\n**By:** {admin_mention}\n**User:** {user_mention}"
        await client.send_message(OTHER_LOGS, log_msg)

    except ChatAdminRequired:
        await message.reply_text("I need admin rights to unmute users.")


# Unmute Button Callback
@app.on_callback_query(filters.regex(r"^unmute_(\d+)$"))
async def unmute_btn_callback(client, cb):
    user_id = int(cb.data.split("_")[1])
    chat_id = cb.message.chat.id
    admin = cb.from_user

    member = await client.get_chat_member(chat_id, admin.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await cb.answer("You're not an admin!", show_alert=True)

    try:
        await client.restrict_chat_member(
            chat_id,
            user_id,
            permissions=enums.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            ),
        )
        await cb.message.edit_text(
            "User unmuted successfully!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        user = await client.get_users(user_id)
        admin_mention = mention(admin.id, admin.first_name)
        user_mention = mention(user_id, user.first_name)
        log_msg = f"**Unmute (Button) Alert**\n\n**Chat:** {cb.message.chat.title} (`{chat_id}`)\n**By:** {admin_mention}\n**User:** {user_mention}"
        await client.send_message(OTHER_LOGS, log_msg)

    except Exception:
        await cb.answer("Failed to unmute the user.", show_alert=True)
