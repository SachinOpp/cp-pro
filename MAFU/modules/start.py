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
        InlineKeyboardButton("• ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ •", callback_data="show_help")
    ]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("• ᴘʀɪᴠᴀᴛᴇ ꜱᴛᴀʀᴛ •", url=f"https://t.me/{BOT_USERNAME}?start=help")
    ]
])

@app.on_message(filters.command("start"))
async def start_command(_, message: Message):
    try:
        user = message.from_user
        chat = message.chat

        # Debugging logs (remove later)
        print(f"Chat Type: {chat.type}")
        print(f"From User: {user.id if user else 'None'}")

        # Add to database
        if user:
            await add_user(user.id)
        if chat.type in ["group", "supergroup"]:
            await add_chat(chat.id)

        # Private message
        if chat.type == "private":
            await message.reply_photo(
                photo=START_IMG,
                caption=get_start_caption(user),
                reply_markup=START_BUTTONS
            )
        else:
            await message.reply_text(
                text=f"**ʜᴇʏ {user.mention if user else 'ᴜꜱᴇʀ'}, ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**",
                reply_markup=PRIVATE_START_BUTTON
            )
    except Exception as e:
        print(f"Error in /start: {e}")
