from pyrogram.types import ChatPermissions
from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid, UserNotParticipant, UserAlreadyParticipant
from MAFU import MAFU as app
from MAFU.helper.admin import is_admins

FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)

@app.on_message(filters.command("mute", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
@is_admins
async def mute_command_handler(client, message):
    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        # force mute anyway (don't skip if already muted)
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)

        msg = f"User muted successfully.\n\nMuted by: {admin_mention}\nUser: {user_mention}"
        if reason:
            msg += f"\n\nReason: {reason}"

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


@app.on_callback_query(filters.regex(r"^unmute_(\d+)$"))
async def unmute_callback(client, callback_query):
    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id
    from_user = callback_query.from_user  

    chat_member = await client.get_chat_member(chat_id, from_user.id)
    if chat_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await callback_query.answer("You are not an admin!", show_alert=True)

    try:
        await client.restrict_chat_member(chat_id, user_id, FULL_PERMISSIONS)
        await callback_query.message.edit_text(
            "User unmuted successfully.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]])
        )
    except Exception:
        await callback_query.answer("Failed to unmute the user!", show_alert=True)


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
