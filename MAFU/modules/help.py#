from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from MAFU import MAFU as app

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    if message.chat.type != "private":
        bot_user = await client.get_me()
        return await message.reply(
            "**ᴘʟᴇᴀsᴇ ᴜsᴇ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ғᴏʀ ʜᴇʟᴘ.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Click Here •", url=f"t.me/{bot_user.username}?start=help")]
            ])
        )

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
