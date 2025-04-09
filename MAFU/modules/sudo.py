from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from MAFU.helper.sudo import add_sudo, remove_sudo, get_sudoers
from config import OWNER_ID
from MAFU import MAFU as app


async def extract_user_id(message: Message) -> int:
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    if len(message.command) >= 2:
        user = message.command[1]
        if user.startswith("@"):
            try:
                user_obj = await message._client.get_users(user)
                return user_obj.id
            except Exception:
                return None
        else:
            try:
                return int(user)
            except ValueError:
                return None
    return None


@app.on_message(filters.command("sudo") & filters.user(OWNER_ID))
async def addsudo_cmd(client, message):
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply("Please specify a user to add to the SUDO list!")

    await add_sudo(user_id)
    await message.reply(f"✅ `{user_id}` has been added to the SUDO list.")


@app.on_message(filters.command("rmsudo") & filters.user(OWNER_ID))
async def delsudo_cmd(client, message):
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply("Please specify a user to remove from the SUDO list!")

    await remove_sudo(user_id)
    await message.reply(f"❌ `{user_id}` has been removed from the SUDO list.")


@app.on_message(filters.command("sudolist") & filters.user(OWNER_ID))
async def sudolist_cmd(client, message: Message):
    sudoers = await get_sudoers()

    if not sudoers:
        return await message.reply("No SUDO users found.")

    text = "**👑 SUDO Users:**\n\n"
    for uid in sudoers:
        try:
            user = await client.get_users(uid)
            name = f"{user.first_name} (`{user.id}`)"
        except:
            name = f"`{uid}`"
        text += f"• {name}\n"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )

    await message.reply(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"^close_sudo_list$"))
async def close_sudo_list_callback(client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except:
        await callback_query.answer("Failed to delete message.", show_alert=True)
