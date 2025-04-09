from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from MAFU import MAFU as app

@app.on_callback_query(filters.regex("close"))
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
        closed = await query.message.reply_text(
            f"✅ Closed by : {query.from_user.mention}"
        )
        await asyncio.sleep(2)
        await closed.delete()
    except:
        pass
