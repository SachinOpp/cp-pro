from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType
from MAFU import MAFU as app
from MAFU.helper.database import get_settings, save_settings
from pyrogram.errors.exceptions.forbidden_403 import ChatAdminRequired

# Settings Menu - /settings
@app.on_message(filters.command("settings") & filters.group)
async def settings_command(_, message: Message):
    user = message.from_user
    chat = message.chat

    # Check admin
    try:
        member = await app.get_chat_member(chat.id, user.id)
        if member.status not in ("administrator", "creator"):
            return await message.reply_text("⛔ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴀᴄᴄᴇꜱꜱ ꜱᴇᴛᴛɪɴɢꜱ.")
    except ChatAdminRequired:
        return await message.reply_text("I need admin rights to manage settings.")

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

# Toggle Rules Filter
@app.on_callback_query(filters.regex(r"^toggle_rules_(\d+)$"))
async def toggle_rules(_, query: CallbackQuery):
    chat_id = int(query.matches[0].group(1))
    user = query.from_user

    member = await app.get_chat_member(chat_id, user.id)
    if member.status not in ("administrator", "creator"):
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

# Set Group Rules Prompt
@app.on_callback_query(filters.regex(r"^set_rules_(\d+)$"))
async def prompt_set_rules(_, query: CallbackQuery):
    chat_id = int(query.matches[0].group(1))
    user = query.from_user

    member = await app.get_chat_member(chat_id, user.id)
    if member.status not in ("administrator", "creator"):
        return await query.answer("Only admins can do this.", show_alert=True)

    await query.message.edit_text(
        "Please send the new group rules in your next message.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel", callback_data=f"go_back_settings_{chat_id}")]
        ])
    )

    # Save waiting state in memory or DB
    app.set_attr(f"waiting_rules_{user.id}", chat_id)

# Receive Rules Text
@app.on_message(filters.text & filters.group)
async def save_rules_text(_, message: Message):
    user = message.from_user
    chat = message.chat

    attr_name = f"waiting_rules_{user.id}"
    if not hasattr(app, attr_name):
        return

    expected_chat_id = getattr(app, attr_name)
    if expected_chat_id != chat.id:
        return

    await save_settings(chat.id, "group_rules", message.text)
    delattr(app, attr_name)
    await message.reply_text("✅ Group rules updated successfully!")

# Go Back to Settings
@app.on_callback_query(filters.regex(r"^go_back_settings_(\d+)$"))
async def go_back_settings(_, query: CallbackQuery):
    chat_id = int(query.matches[0].group(1))
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
