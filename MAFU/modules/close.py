from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from MAFU import MAFU as app

@app.on_message(filters.command("test"))
async def test_cmd(_, message: Message):
    await message.reply_text(
        "ᴀᴇ ʙᴀʙᴜ, ʏᴇ ᴛᴇꜱᴛ ʜᴀɪ...",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]]
        )
    )

@app.on_callback_query(filters.regex("close"))
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
        closed = await query.message.reply_text(
            f"ᴄʟᴏꜱᴇᴅ ʙʏ : {query.from_user.mention}"
        )
        await asyncio.sleep(2)
        await closed.delete()
    except:
        pass
