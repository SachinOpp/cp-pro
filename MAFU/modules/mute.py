from pyrogram import Client, filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired
from MAFU import MAFU as app
from typing import Tuple, Optional
from MAFU.helper.admin import is_admins
'''
# =================== ADMIN DECORATOR ===================
def is_admins(func):
    async def wrapper(client, message: Message):
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                return await message.reply_text("Only admins can use this command.")
        except Exception:
            return await message.reply_text("Failed to check admin status.")
        return await func(client, message)
    return wrapper
'''
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
@is_admins
async def mute_command_handler(client, message):
    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        target = await client.get_chat_member(message.chat.id, user_id)
        if target.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text("**You can't mute an admin!**")
    except Exception as e:
        return await message.reply_text(f"**Failed to fetch user info:** `{e}`")

    try:
        await client.restrict_chat_member(message.chat.id, user_id, MUTE_PERMISSIONS)
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

    except ChatAdminRequired:
        await message.reply_text(
            "I need to be an admin with mute permissions!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )

# =================== UNMUTE BY BUTTON ===================
@app.on_callback_query(filters.regex(r"^unmute_(\d+)$"))
async def unmute_callback(client, callback_query):
    try:
        user_id = int(callback_query.data.split("_")[1])
        chat_id = callback_query.message.chat.id
        admin_id = callback_query.from_user.id

        # Check if the person clicking is admin
        chat_member = await client.get_chat_member(chat_id, admin_id)
        if chat_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await callback_query.answer("❖ You are not an admin!", show_alert=True)

        # Unmute the user (don't set until_date to avoid 'NoneType' error)
        await client.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )

        # Fetch user details for mention
        user = await client.get_users(user_id)
        mention = f"[{user.first_name}](tg://user?id={user.id})"

        # Edit original message
        await callback_query.message.edit_text(
            f"{mention} User unmuted successfully.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close")]
            ]),
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"Unmute error: {e}")
        await callback_query.answer("❖ Failed to unmute the user!", show_alert=True)
        
# =================== UNMUTE BY COMMAND ===================
@app.on_message(filters.command("unmute", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
@is_admins
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
    except ChatAdminRequired:
        await message.reply_text(
            "I need admin privileges to unmute users!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )
