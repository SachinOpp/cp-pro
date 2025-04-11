from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from MAFU import MAFU as app

HELP_COMMANDS = {
    "mute_unmute": "Mute: `/mute @user`, Unmute: `/unmute @user`",
    "ban": "Ban: `/ban @user`, Unban: `/unban @user`",
    "promote_demote": "Promote: `/promote @user`, Demote: `/demote @user`",
    "fullpromote": "FullPromote: `/fullpromote @user`",
    "edit": "Edit: `/edit <old msg> <new msg>`",
    "joinmode": "JoinMode: `/joinmode on/off`",
    "warn": "Warn: `/warn @user`"
}

@app.on_message(filters.command("help"))
async def help_command(_, message: Message):
    if message.chat.type != "private":
        return await message.reply("**ᴘʟᴇᴀsᴇ ᴜsᴇ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ғᴏʀ ʜᴇʟᴘ.**", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Click Here •", url=f"t.me/{app.me.username}?start=help")]
        ]))

    await message.reply_text(
        "**❖ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ɴᴇᴇᴅ ʜᴇʟᴘ.**\n**● ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ](https://t.me/Copyright_Community)**",
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
            ]
        ])
    )

@app.on_callback_query(filters.regex(r"help_(\w+)"))
async def command_help(_, query: CallbackQuery):
    command = query.matches[0].group(1)
    help_text = HELP_COMMANDS.get(command, "No help found for this command.")
    await query.message.edit_text(
        f"**❖ Help Menu: `{command}`**\n\n{help_text}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Back to Help •", callback_data="show_help")]
        ])
    )

@app.on_callback_query(filters.regex("show_help"))
async def show_main_help(_, query: CallbackQuery):
    await query.message.edit_text(
        "**❖ ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ʜᴇʟᴘ.**\n**● ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ](https://t.me/Copyright_Community)**",
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
