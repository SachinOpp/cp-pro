from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import OWNER_ID, BOT_USERNAME
from MAFU import MAFU as app
from MAFU.helper.database import add_user, add_chat

START_IMG = "https://files.catbox.moe/jhlnjc.jpg"

# Start caption with user and bot mention
def get_start_caption(user, bot):
    return f"""
**✨ ʜᴇʏ {user.mention}, ʙᴀʙʏ! ✨**

ɪ'ᴍ [{BOT_USERNAME}](https://t.me/{BOT_USERNAME}) – ʏᴏᴜʀ ʟᴏʏᴀʟ ᴀɪ ɢᴜᴀʀᴅ ʀᴇᴀᴅʏ ᴛᴏ ꜱᴇʀᴠᴇ ʏᴏᴜ!

ɪ ᴄᴀɴ:
• ꜱᴛᴏᴘ ꜱᴘᴀᴍᴍᴇʀꜱ
• ꜱᴇɴᴅ ᴡᴀʀɴɪɴɢꜱ
• ᴅᴇꜰᴇɴᴅ ʏᴏᴜʀ ɢʀᴏᴜᴘ
• ᴀɴᴅ ᴇᴠᴇɴ ᴡʜɪꜱᴘᴇʀ ꜱᴇᴄʀᴇᴛꜱ...

➥ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱɪᴛ ʙᴀᴄᴋ, ʟᴇᴀᴠᴇ ᴛʜᴇ ʀᴇꜱᴛ ᴛᴏ ᴍᴇ!

**— ᴡɪᴛʜ ʟᴏᴠᴇ, ʏᴏᴜʀ ᴠɪʀᴛᴜᴀʟ ᴘʀᴏᴛᴇᴄᴛᴏʀ**
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("• ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [
        InlineKeyboardButton("• ʜᴇʟᴘ •", callback_data="show_help"),
        InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="show_about")
    ],
    [InlineKeyboardButton("• ᴏᴡɴᴇʀ •", user_id=OWNER_ID)]
])

# /start command
@app.on_message(filters.command("start"))
async def start_command(_, message: Message):
    if message.chat.type.name == "PRIVATE":
        await add_user(message.from_user.id)
        caption = get_start_caption(message.from_user, app.me)
        return await message.reply_photo(
            photo=START_IMG,
            caption=caption,
            reply_markup=START_BUTTONS
        )
    else:
        await add_chat(message.chat.id)
        return await message.reply(
            "**ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**\n\nɪ'ᴍ ɴᴏᴡ ᴀᴄᴛɪᴠᴇ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴀɴᴅ ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ."
        )

# /help command
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from config import BOT_USERNAME
from MAFU import MAFU as app

START_IMG = "https://files.catbox.moe/jhlnjc.jpg"

HELP_TEXT = (
    "**❖ Help Menu ⏤͟͟͞͞★**\n\n"
    "● `/start` ➥ Start the bot and check if it's alive.\n"
    "● `/ping` ➥ Check the bot's response time.\n"
    "● `/repo` ➥ View the bot's source code.\n"
    "● `/joinmode` ➥ Configure how new members join.\n"
    "● `/ban`, `/unban` ➥ Ban or unban users from your group.\n"
    "● `/mute`, `/unmute` ➥ Mute or unmute group members.\n"
    "● `/promote`, `/demote`, `/fullpromote` ➥ Change user roles in your group.\n"
    "● `/edit` ➥ Edit a previously sent message.\n"
    "● `/biobot` ➥ Activate the chatbot/auto-reply feature."
)

# /help command
@app.on_message(filters.command("help"))
async def help_command(_, message: Message):
    if message.chat.type.name != "PRIVATE":
        return await message.reply(
            "**Help command is only available in private chat.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Open DM •", url=f"https://t.me/{BOT_USERNAME}?start=help")]
            ])
        )

    await message.reply_photo(
        photo=START_IMG,
        caption=HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Back •", callback_data="go_back")]
        ])
    )
# Help via button
@app.on_callback_query(filters.regex("show_help"))
async def show_help(_, query: CallbackQuery):
    await query.message.edit_media(
        media=query.message.photo.file_id if query.message.photo else START_IMG,
        caption=HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Back •", callback_data="go_back")]
        ])
    )

# About via button
@app.on_callback_query(filters.regex("show_about"))
async def show_about(_, query: CallbackQuery):
    await query.message.edit_caption(
        "**❖ ᴀʙᴏᴜᴛ ᴍᴇ ⏤͟͟͞͞★\n\nɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ ᴡɪᴛʜ ᴀɴᴛɪ-ᴘᴏʀɴ, sᴘᴀᴍ ᴀɴᴅ ᴍᴏʀᴇ**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="go_back")]
        ])
    )

# Back to Start
@app.on_callback_query(filters.regex("go_back"))
async def go_back(_, query: CallbackQuery):
    try:
        await query.message.edit_media(
            media=InputMediaPhoto(
                media=START_IMG,
                caption=START_CAPTION
            ),
            reply_markup=START_BUTTONS
        )
    except Exception:
        await query.message.edit_caption(
            caption=START_CAPTION,
            reply_markup=START_BUTTONS
        )
