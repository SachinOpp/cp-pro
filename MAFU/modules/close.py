import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

close_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton("✖️ Close", callback_data="close")]]
)

@Client.on_callback_query(filters.regex("close"))
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
        umm = await query.message.reply_text(
            f"ᴄʟᴏꜱᴇᴅ ʙʏ : {query.from_user.mention}"
        )
        await asyncio.sleep(2)
        await umm.delete()
    except:
        pass
