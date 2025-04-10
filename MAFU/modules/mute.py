from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired
from MAFU import MAFU as app
from config import OTHER_LOGS, BOT_USERNAME

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

# Check if the user has permission to restrict others
async def can_restrict_members(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status == "creator":
            return True
        elif member.status == "administrator":
            return getattr(member.privileges, "can_restrict_members", False)
        return False
    except:
        return False

# Check if target user is admin
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

# Extract target user and reason
async def extract_user_and_reason(message, client):
    user_id = None
    first_name = None
    reason = None

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if not user:
            await message.reply_text("⚠️ Replied user not found.")
            return None, None, None
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
            await message.reply_text(f"⚠️ Cannot find this user: `{user_identifier}`")
            return None, None, None
    else:
        await message.reply_text("⚠️ Please reply to a user or use /mute @username.")
        return None, None, None

    return user_id, first_name, reason

# MUTE COMMAND
@app.on_message(filters.command("mute"))
async def mute_command(client, message):
    if not await can_restrict_members(client, message.chat.id, message.from_user.id):
        return await message.reply("❌ You must be an admin with 'restrict members' permission to use this command!")

    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    if await is_admin(client, message.chat.id, user_id):
        return await message.reply("⚠️ You cannot mute an admin!")

    try:
        await client.restrict_chat_member(message.chat.id, user_id, MUTE_PERMISSIONS)
        user = await client.get_users(user_id)

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
async def unmute_command(client, message):
    if not await can_restrict_members(client, message.chat.id, message.from_user.id):
        return await message.reply("❌ You must be an admin with 'restrict members' permission to use this command!")

    user_id, first_name, _ = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.restrict_chat_member(message.chat.id, user_id, FULL_PERMISSIONS)
        await message.reply(
            f"{mention(user_id, first_name)} has been unmuted.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

        user = await client.get_users(user_id)
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

# UNMUTE BUTTON
@app.on_callback_query(filters.regex(r"^unmute_(\d+)$"))
async def unmute_button(client, callback_query):
    if not await can_restrict_members(client, callback_query.message.chat.id, callback_query.from_user.id):
        return await callback_query.answer("❌ You must be an admin with 'restrict members' permission!", show_alert=True)

    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id

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
