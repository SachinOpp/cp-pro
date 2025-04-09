from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid, UserNotParticipant, UserAlreadyParticipant
from MAFU import MAFU as app
from MAFU.helper.admin import is_admins

def mention(user_id, name):
    return f"[{name}](tg://user?id={user_id})"

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
            await message.reply_text("I can't find that user!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))
            return None, None, None

    if not user:
        await message.reply_text("Please mention a valid user or reply to their message!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))
        return None, None, None

    try:
        chat_member = await client.get_chat_member(message.chat.id, user.id)
    except UserNotParticipant:
        pass
    else:
        if chat_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await message.reply_text("This user is a staff member and cannot be muted or banned!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))
            return None, None, None

    return user.id, user.first_name, reason


@app.on_message(filters.command("ban", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def ban_command_handler(client, message):
    if not await is_admins(client, message):
        return await message.reply_text("You are not an admin!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))

    user_id, first_name, reason = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        chat_member = await client.get_chat_member(message.chat.id, user_id)
        if chat_member.status == enums.ChatMemberStatus.BANNED:
            # First unban the user to allow re-ban
            await client.unban_chat_member(message.chat.id, user_id)

        await client.ban_chat_member(message.chat.id, user_id)
        user_mention = mention(user_id, first_name)
        admin_mention = mention(message.from_user.id, message.from_user.first_name)
        msg = f"**User Banned Successfully**\n\n**Banned by:** {admin_mention}\n**User:** {user_mention}"

        if reason:
            msg += f"\n**Reason:** {reason}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Unban", callback_data=f"unban_{user_id}")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        await message.reply_text(msg, reply_markup=keyboard, disable_web_page_preview=True)

    except ChatAdminRequired:
        await message.reply_text("I need to be an admin with ban permissions!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))


@app.on_callback_query(filters.regex(r"^unban_(\d+)$"))
async def unban_callback(client, callback_query):
    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id
    from_user = callback_query.from_user

    chat_member = await client.get_chat_member(chat_id, from_user.id)
    if chat_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await callback_query.answer("You are not an admin!", show_alert=True)

    try:
        await client.unban_chat_member(chat_id, user_id)
        await callback_query.message.edit_text("User unbanned successfully!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))
    except Exception:
        await callback_query.answer("Failed to unban the user!", show_alert=True)


@app.on_message(filters.command("unban", prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def unban_user(client, message):
    if not await is_admins(client, message):
        return await message.reply_text("You are not an admin!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))

    user_id, first_name, _ = await extract_user_and_reason(message, client)
    if not user_id:
        return

    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"{mention(user_id, first_name)} has been successfully unbanned!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))
    except ChatAdminRequired:
        await message.reply_text("I need admin privileges to unban users!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close")]]))
