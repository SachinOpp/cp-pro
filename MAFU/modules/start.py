from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import OWNER_ID, BOT_USERNAME
from MAFU import app

START_IMG = "https://files.catbox.moe/jhlnjc.jpg"
START_CAPTION = "**✨ ʜᴇʏ ʙᴀʙʏ! ɪ'ᴍ ᴀʟɪᴠᴇ ᴀɴᴅ ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✨**"

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
    if message.chat.type.name != "PRIVATE":
        return await message.reply(
            "**ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ᴍʏ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ᴄʟɪᴄᴋ ʜᴇʀᴇ •", url=f"https://t.me/{BOT_USERNAME}?start=start")]
            ])
        )
    await message.reply_photo(
        photo=START_IMG,
        caption=START_CAPTION,
        reply_markup=START_BUTTONS
    )

# /help command
@app.on_message(filters.command("help"))
async def help_command(_, message: Message):
    if message.chat.type.name != "PRIVATE":
        return await message.reply(
            "**ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴅᴍ.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ᴏᴘᴇɴ ᴅᴍ •", url=f"https://t.me/{BOT_USERNAME}?start=help")]
            ])
        )

    await message.reply_text(
        "**❖ ʜᴇʟᴘ ᴍᴇɴᴜ ⏤͟͟͞͞★**\n\n"
        "**● /start ➥ sᴛᴀʀᴛ ʙᴏᴛ\n"
        "● /ping ➥ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴘɪɴɢ\n"
        "● /repo ➥ ʀᴇᴘᴏ ʟɪɴᴋ**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="go_back")]
        ])
    )

# Help via button
@app.on_callback_query(filters.regex("show_help"))
async def show_help(_, query: CallbackQuery):
    await query.message.edit_caption(
        "**❖ ʜᴇʟᴘ ᴍᴇɴᴜ ⏤͟͟͞͞★**\n\n"
        "● /start ➥ sᴛᴀʀᴛ ʙᴏᴛ\n"
        "● /ping ➥ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴘɪɴɢ\n"
        "● /repo ➥ ʀᴇᴘᴏ ʟɪɴᴋ",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="go_back")]
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
    await query.message.edit_caption(
        START_CAPTION,
        reply_markup=START_BUTTONS
    )
