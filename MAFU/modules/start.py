from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message
from config import OWNER_ID, BOT_USERNAME
from MAFU import MAFU as app
from MAFU.helper.database import add_user, add_chat

START_IMG = "https://files.catbox.moe/jhlnjc.jpg"

def get_start_caption(user):
    return f"""
**✨ ʜᴇʏ {user.mention}, ʙᴀʙʏ! ✨**
ɪ'ᴍ [{BOT_USERNAME}](https://t.me/{BOT_USERNAME}) – ʏᴏᴜʀ ʟᴏʏᴀʟ ᴀɪ ɢᴜᴀʀᴅ ʀᴇᴀᴅʏ ᴛᴏ ꜱᴇʀᴠᴇ ʏᴏᴜ!

ɪ ᴄᴀɴ:
• ꜱᴛᴏᴘ ꜱᴘᴀᴍᴍᴇʀꜱ • ꜱᴇɴᴅ ᴡᴀʀɴɪɴɢꜱ
• ᴅᴇꜰᴇɴᴅ ʏᴏᴜʀ ɢʀᴏᴜᴘ
• ᴀɴᴅ ᴇᴠᴇɴ ᴡʜɪꜱᴘᴇʀ ꜱᴇᴄʀᴇᴛꜱ...
➥ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱɪᴛ ʙᴀᴄᴋ, ʟᴇᴀᴠᴇ ᴛʜᴇ ʀᴇꜱᴛ ᴛᴏ ᴍᴇ!

**— ᴡɪᴛʜ ʟᴏᴠᴇ, ʏᴏᴜʀ ᴠɪʀᴛᴜᴀʟ ᴘʀᴏᴛᴇᴄᴛᴏʀ**
"""

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("• ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
    ],
    [
        InlineKeyboardButton("• ʟᴏɢs •", url="https://t.me/Copyright_logs"),
        InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇ •", url="https://t.me/Copyright_Community")
    ],
    [
        InlineKeyboardButton("• ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ •", callback_data="show_help")]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("• ᴘʀɪᴠᴀᴛᴇ ꜱᴛᴀʀᴛ •", url=f"https://t.me/{BOT_USERNAME}?start=help")
    ]
])

@app.on_message(filters.command("start"))
async def start_command(_, message: Message):
    if message.chat.type.name == "PRIVATE":
        await add_user(message.from_user.id)
        caption = get_start_caption(message.from_user)
        return await message.reply_photo(
            photo=START_IMG,
            caption=caption,
            reply_markup=START_BUTTONS
        )
    else:
        return await message.reply(
            "**ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ /start ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏ.**",
            reply_markup=PRIVATE_START_BUTTON
        )

@app.on_message(filters.new_chat_members)
async def group_welcome(_, message: Message):
    for member in message.new_chat_members:
        if member.id == (await app.get_me()).id:
            await add_chat(message.chat.id)
            try:
                await add_user(message.from_user.id)
            except:
                pass
            caption = f"""
**ᴛʜᴀɴᴋꜱ {message.from_user.mention} ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**
ɪ'ᴍ ɴᴏᴡ ᴀᴄᴛɪᴠᴇ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴀɴᴅ ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ.
➥ ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴍʏ ꜱᴇᴛᴛɪɴɢꜱ ᴀɴᴅ ɢɪᴠᴇ ᴘʀᴏᴘᴇʀ ʀɪɢʜᴛꜱ.
"""
            await message.reply_photo(
                photo=START_IMG,
                caption=caption,
                reply_markup=START_BUTTONS
            )

@app.on_callback_query(filters.regex("go_back"))
async def go_back(_, query):
    caption = get_start_caption(query.from_user)
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMG,
            caption=caption
        ),
        reply_markup=START_BUTTONS
    )
