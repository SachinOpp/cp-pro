from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from config import OWNER_ID, BOT_USERNAME
import config
from MAFU import MAFU as app


START_IMG = "https://files.catbox.moe/jhlnjc.jpg"
START_CAPTION = "**✨ ʜᴇʏ ʙᴀʙʏ! ɪ'ᴍ ᴀʟɪᴠᴇ ᴀɴᴅ ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✨**"

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("• ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [
        InlineKeyboardButton("• ʜᴇʟᴘ •", callback_data="show_help"),
        InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="show_about")
    ],
    [
        InlineKeyboardButton("• ᴏᴡɴᴇʀ •", user_id=config.OWNER_ID)
    ]
])


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply_photo(
        photo=START_IMG,
        caption=START_CAPTION,
        reply_markup=START_BUTTONS
    )


@app.on_callback_query(filters.regex("show_help"))
async def show_help(_, query: CallbackQuery):
    await query.message.edit_caption(
        "**❖ ʜᴇʟᴘ ᴍᴇɴᴜ ⏤͟͟͞͞★\n\n● /start ➥ sᴛᴀʀᴛ ʙᴏᴛ\n● /ping ➥ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴘɪɴɢ\n● /repo ➥ ʀᴇᴘᴏ ʟɪɴᴋ**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="go_back")]
        ])
    )


@app.on_callback_query(filters.regex("show_about"))
async def show_about(_, query: CallbackQuery):
    await query.message.edit_caption(
        "**❖ ᴀʙᴏᴜᴛ ᴍᴇ ⏤͟͟͞͞★\n\nɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ ᴡɪᴛʜ ᴀɴᴛɪ-ᴘᴏʀɴ, sᴘᴀᴍ ᴀɴᴅ ᴍᴏʀᴇ**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="go_back")]
        ])
    )


@app.on_callback_query(filters.regex("go_back"))
async def go_back(_, query: CallbackQuery):
    await query.message.edit_caption(
        START_CAPTION,
        reply_markup=START_BUTTONS
    )
