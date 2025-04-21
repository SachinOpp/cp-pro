from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from MAFU import MAFU as app
from MAFU.helper.admin import is_admins
from MAFU.helper.database import get_settings, save_settings

# /settings command
@app.on_message(filters.command("settings") & filters.group)
async def settings_command(_, message: Message):
    user = message.from_user
    chat = message.chat

    if not await is_admins(chat.id, user.id):
        return await message.reply_text("⛔ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴀᴄᴄᴇꜱꜱ ꜱᴇᴛᴛɪɴɢꜱ.")

    settings = await get_settings(chat.id)
    rules_filter = settings.get("rules_filter", True)

    await message.reply_text(
        f"**⚙️ Group Settings for {chat.title}**\n\n"
        f"**Rules Filter:** {'✅ ON' if rules_filter else '❌ OFF'}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Toggle Rules Filter", callback_data=f"toggle_rules_{chat.id}")],
            [InlineKeyboardButton("Set Group Rules", callback_data=f"set_rules_{chat.id}")]
        ])
    )

# Toggle rules ON/OFF
@app.on_callback_query(filters.regex(r"^toggle_rules_(\d+)$"))
async def toggle_rules(_, query: CallbackQuery):
    chat_id = int(query.matches[0].group(1))
    user = query.from_user

    if not await is_admins(chat_id, user.id):
        return await query.answer("Only admins can do this.", show_alert=True)

    settings = await get_settings(chat_id)
    current = settings.get("rules_filter", True)
    new_setting = not current
    await save_settings(chat_id, "rules_filter", new_setting)

    await query.edit_message_text(
        f"**⚙️ Updated Settings**\n\n"
        f"**Rules Filter:** {'✅ ON' if new_setting else '❌ OFF'}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Toggle Rules Filter", callback_data=f"toggle_rules_{chat_id}")],
            [InlineKeyboardButton("Set Group Rules", callback_data=f"set_rules_{chat_id}")]
        ])
    )
    await query.answer("Setting Updated!")

# Prompt to set rules
@app.on_callback_query(filters.regex(r"^set_rules_(\d+)$"))
async def prompt_set_rules(_, query: CallbackQuery):
    chat_id = int(query.matches[0].group(1))
    user = query.from_user

    if not await is_admins(chat_id, user.id):
        return await query.answer("Only admins can do this.", show_alert=True)

    await query.message.edit_text(
        "📝 Please send the new group rules in your next message.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel", callback_data=f"go_back_settings_{chat_id}")]
        ])
    )

    app.set_attr(f"waiting_rules_{user.id}", chat_id)

# Back to settings menu
@app.on_callback_query(filters.regex(r"^go_back_settings_(\d+)$"))
async def go_back_settings(_, query: CallbackQuery):
    chat_id = int(query.matches[0].group(1))

    if not await is_admins(chat_id, query.from_user.id):
        return await query.answer("Only admins can do this.", show_alert=True)

    settings = await get_settings(chat_id)
    rules_filter = settings.get("rules_filter", True)

    await query.message.edit_text(
        f"**⚙️ Group Settings for this chat**\n\n"
        f"**Rules Filter:** {'✅ ON' if rules_filter else '❌ OFF'}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Toggle Rules Filter", callback_data=f"toggle_rules_{chat_id}")],
            [InlineKeyboardButton("Set Group Rules", callback_data=f"set_rules_{chat_id}")]
        ])
    )

# Receive the new rules from admin
@app.on_message(filters.text & filters.group)
async def set_rules_text(_, message: Message):
    user = message.from_user
    chat = message.chat

    waiting = app.get_attr(f"waiting_rules_{user.id}")
    if waiting and waiting == chat.id:
        await save_settings(chat.id, "rules_text", message.text)
        await message.reply_text("✅ Rules updated successfully!")
        app.del_attr(f"waiting_rules_{user.id}")
