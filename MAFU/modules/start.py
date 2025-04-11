from pyrogram import filters, Client
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaPhoto,
    Message,
)
from config import OWNER_ID, BOT_USERNAME
from MAFU import MAFU as app
from MAFU.helper.database import add_user, add_chat


START_IMG = "https://files.catbox.moe/jhlnjc.jpg"

# Start caption with user and bot mention
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

# /start command
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
        await add_chat(message.chat.id)
        return await message.reply(
            "**ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**\n\nɪ'ᴍ ɴᴏᴡ ᴀᴄᴛɪᴠᴇ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ ᴀɴᴅ ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ."
        )

# Help Texts
HELP_COMMANDS = {
    "mute_unmute": "`/mute`, `/unmute` ➥ Mute or unmute group members.",
    "ban": "`/ban`, `/unban` ➥ Ban or unban users from your group.",
    "promote_demote": "`/promote`, `/demote` ➥ Promote or demote users.",
    "fullpromote": "`/fullpromote` ➥ Give full admin rights to user.",
    "edit": "`/edit` ➥ Edit a previously sent message.",
    "joinmode": "`/joinmode` ➥ Configure how new members join.",
    "warn": "`/warn`, `/resetwarns` ➥ Warn users or reset their warnings."
}

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
        caption="**❖ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ.**\n**● ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ](https://t.me/Copyright_Community).**\n**● ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: [ !, ., / ]**",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Mute / Unmute", callback_data="help_mute_unmute"),
                InlineKeyboardButton("Ban", callback_data="help_ban")
            ],
            [
                InlineKeyboardButton("Promote / Demote", callback_data="help_promote_demote")
            ],
            [
                InlineKeyboardButton("FullPromote", callback_data="help_fullpromote")
            ],
            [
                InlineKeyboardButton("Edit", callback_data="help_edit"),
                InlineKeyboardButton("JoinMode", callback_data="help_joinmode"),
                InlineKeyboardButton("Warn", callback_data="help_warn")
            ],
            [
                InlineKeyboardButton("• Back •", callback_data="go_back")
            ]
        ])
    )

# Help via callback buttons
@app.on_callback_query(filters.regex(r"help_(\w+)"))
async def command_help(_, query: CallbackQuery):
    command = query.matches[0].group(1)
    help_text = HELP_COMMANDS.get(command, "No help found for this command.")

    await query.message.edit_text(
        f"**❖ Help Menu: `{command}`**\n\n{help_text}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Back to Help •", callback_data="show_help")],
        ])
    )

# Show main help again
@app.on_callback_query(filters.regex("show_help"))
async def show_main_help(_, query: CallbackQuery):
    await query.message.edit_text(
        "**❖ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ.**\n**● ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ](https://t.me/Copyright_Community).**\n**● ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ: [ !, ., / ]**",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Mute | Unmute", callback_data="help_mute_unmute"),
                InlineKeyboardButton("Ban | Unban", callback_data="help_ban")
            ],
            [
                InlineKeyboardButton("Promote | Demote", callback_data="help_promote_demote")
            ],
            [
                InlineKeyboardButton("FullPromote", callback_data="help_fullpromote")
            ],
            [
                InlineKeyboardButton("Edit", callback_data="help_edit"),
                InlineKeyboardButton("JoinMode", callback_data="help_joinmode"),
                InlineKeyboardButton("Warn", callback_data="help_warn")
            ],
            [
                InlineKeyboardButton("• Back •", callback_data="go_back")
            ]
        ])
    )
    
# Help via button
@app.on_callback_query(filters.regex("show_help"))
async def show_help(_, query: CallbackQuery):
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMG,
            caption=HELP_TEXT
        ),
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
            [InlineKeyboardButton("• Back •", callback_data="go_back")]
        ])
    )

# Back to Start
@app.on_callback_query(filters.regex("go_back"))
async def go_back(_, query: CallbackQuery):
    caption = get_start_caption(query.from_user)
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMG,
            caption=caption
        ),
        reply_markup=START_BUTTONS
    )
