from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    InputMediaPhoto, CallbackQuery, Message
)
from pyrogram.enums import ChatType
from config import OWNER_ID, BOT_USERNAME
from MAFU import MAFU as app
from MAFU.helper.database import add_user, add_chat

START_IMG = "https://files.catbox.moe/jhlnjc.jpg"

# Caption Function
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

# Inline Keyboards
START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("• ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [
        InlineKeyboardButton("• ʟᴏɢs •", url="https://t.me/Copyright_logs"),
        InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇ •", url="https://t.me/Copyright_Community")
    ],
    [InlineKeyboardButton("• ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ •", callback_data="show_help")]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("• ᴘʀɪᴠᴀᴛᴇ ꜱᴛᴀʀᴛ •", url=f"https://t.me/{BOT_USERNAME}?start=help")]
])

# /start Command
@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start_command(_, message: Message):
    user = message.from_user
    chat = message.chat

    await add_user(user.id)
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await add_chat(chat.id)

    if chat.type == ChatType.PRIVATE:
        await message.reply_photo(
            photo=START_IMG,
            caption=get_start_caption(user),
            reply_markup=START_BUTTONS
        )
    else:
        await message.reply_text(
            text=f"**ʜᴇʏ {user.mention}, ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**",
            reply_markup=PRIVATE_START_BUTTON
        )

'''
# Callback: show_help
@app.on_callback_query(filters.regex("show_help"))
async def help_callback(_, callback_query):
    await callback_query.answer()
    await callback_query.message.edit_caption(
        caption=f"""
**🛡 ʜᴇʟᴘ ᴍᴇɴᴜ – ʏᴏᴜʀ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ɢᴜɪᴅᴇ**

**/start** – ʙᴏᴛ ᴄᴏɴꜰɪʀᴍᴀᴛɪᴏɴ & ɪɴᴛʀᴏ  
**/help** – ꜱʜᴏᴡ ᴛʜɪꜱ ᴍᴇɴᴜ  
**/warn [reply/userid]** – ɪꜱꜱᴜᴇ ᴀ ᴡᴀʀɴɪɴɢ  
**/ban [reply/userid]** – ʙᴀɴ ᴀ ᴜꜱᴇʀ  
**/unban [userid]** – ʀᴇᴍᴏᴠᴇ ʙᴀɴ  
**/whisper @user message** – ꜱᴇɴᴅ ᴀ ꜱᴇᴄʀᴇᴛ ᴍᴇꜱꜱᴀɢᴇ  
**/settings** – ᴄᴜꜱᴛᴏᴍɪᴢᴇ ɢʀᴏᴜᴘ ʀᴜʟᴇꜱ  

**ᴍᴏʀᴇ ᴘᴏᴡᴇʀ ꜱᴛᴜꜰꜰ ɪꜱ ᴄᴏᴍɪɴɢ ꜱᴏᴏɴ...**

— ʙʏ [@{BOT_USERNAME}](https://t.me/{BOT_USERNAME})
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="go_back")]
        ])
    )
'''
# Callback: go_back
@app.on_callback_query(filters.regex("go_back"))
async def back_callback(_, callback_query):
    user = callback_query.from_user
    await callback_query.answer()
    await callback_query.message.edit_caption(
        caption=get_start_caption(user),
        reply_markup=START_BUTTONS
    )

'''# /help command
@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message: Message):
    await message.reply_photo(
        photo=START_IMG,
        caption=f"""
**🛡 ʜᴇʟᴘ ᴍᴇɴᴜ – ʏᴏᴜʀ ɢʀᴏᴜᴘ ʀᴜʟᴇꜱ ɢᴜᴀʀᴅ**

**Available Commands:**
/start, /help, /warn, /ban, /unban, /whisper, /settings

ғᴏʀ ɢʀᴏᴜᴘ ꜱᴀꜰᴇᴛʏ, ᴜꜱᴇ ᴍᴇ ᴡɪꜱᴇʟʏ.
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇꜱ •", url="https://t.me/Copyright_Community")],
            [InlineKeyboardButton("• ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ •", callback_data="go_back")]
        ])
    )
'''
#=×=×=×=×=×=×=×=×=×=×=×=×°×=×=×=×=×=×=×°×°=×=×=×=×=×=×=×=×=×=×=§=×=×=×=×=§=§=×=×=×=×=×=×

# Main Help Menu
MAIN_HELP_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("• ʙᴀɴ •", callback_data="help_ban"),
        InlineKeyboardButton("• ᴍᴜᴛᴇ •", callback_data="help_mute"),
        InlineKeyboardButton("• ᴇᴅɪᴛ •", callback_data="help_edit"),
    ],
    [
        InlineKeyboardButton("• ᴀᴅᴍɪɴ •", callback_data="help_admin"),
        InlineKeyboardButton("• ᴀᴜᴛʜ •", callback_data="help_auth"),
    ],
    [
        InlineKeyboardButton("• back •", callback_data="go_back")
    ]
])

@app.on_callback_query(filters.regex("show_help"))
async def show_help_callback(client, query: CallbackQuery):
    await query.message.edit(
        "**Select a Help Category:**",
        reply_markup=MAIN_HELP_MENU
    )

# Help Command
@app.on_message(filters.command("help"))
async def show_help(client, message: Message):
    await message.reply(
        "**Select a Help Category:**",
        reply_markup=MAIN_HELP_MENU
    )


# Ban Callback
@app.on_callback_query(filters.regex("help_ban"))
async def help_ban(client, query: CallbackQuery):
    await query.message.edit(
        text="""
❖ ʙᴀɴ ᴄᴏᴍᴍᴀɴᴅꜱ ➠

❖ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ ʙᴀɴs :

❖ 𝖠𝖣𝖬𝖨𝖭𝖲 𝖮𝖭𝖫𝖸 :

● `/ban` : ʙᴀɴs ᴀ ᴜsᴇʀ. (ʀᴇᴘʟʏ ᴏʀ @ᴜꜱᴇʀɴᴀᴍᴇ)
● `/unban` : ᴜɴʙᴀɴs ᴀ ᴜsᴇʀ (ʀᴇᴘʟʏ ᴏʀ @ᴜꜱᴇʀɴᴀᴍᴇ)

ᴛʜɪs ᴡɪʟʟ ᴡᴏʀᴋ ᴏɴʟʏ ɪꜰ ʙᴏᴛ ʜᴀꜱ ʙᴀɴ ʀɪɢʜᴛs.
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="show_help")]
        ])
    )

# Mute Callback
@app.on_callback_query(filters.regex("help_mute"))
async def help_mute(client, query: CallbackQuery):
    await query.message.edit(
        text="**❖ ᴍᴜᴛᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ➠**\n\n• `/mute` : ᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ\n• `/unmute` : ᴜɴᴍᴜᴛᴇ ᴀ ᴜꜱᴇʀ",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="show_help")]
        ])
    )

# Edit Callback
@app.on_callback_query(filters.regex("help_edit"))
async def help_edit(client, query: CallbackQuery):
    await query.message.edit(
        text="**❖ ᴇᴅɪᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ➠**\n\n• `/editsnipe` : ꜱʜᴏᴡ ʟᴀꜱᴛ ᴇᴅɪᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ\n• `/editlog` : ꜱᴇᴇ ᴇᴅɪᴛ ʟᴏɢ",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="show_help")]
        ])
    )

# Admin Callback
@app.on_callback_query(filters.regex("help_admin"))
async def help_admin(client, query: CallbackQuery):
    await query.message.edit(
        text="**❖ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ ➠**\n\n• `/promote`\n• `/demote`\n• `/admins`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="show_help")]
        ])
    )

# Auth Callback
@app.on_callback_query(filters.regex("help_auth"))
async def help_auth(client, query: CallbackQuery):
    await query.message.edit(
        text="**❖ ᴀᴜᴛʜ ᴜꜱᴇʀꜱ ➠**\n\n• `/auth add` @user\n• `/auth remove` @user\n• `/auth list`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="show_help")]
        ])
    )
