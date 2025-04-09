from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from MAFU.helper.database import get_users, get_chats, get_new_users, get_new_chats
from MAFU import MAFU as app

@Client.on_message(filters.command("stats") & filters.private)
async def stats(_, message: Message):
    users_data = await get_users()
    chats_data = await get_chats()
    new_users = await get_new_users()
    new_chats = await get_new_chats()

    total_users = len(users_data["users"])
    total_chats = len(chats_data["chats"])

    text = f"""**📊 Bot Stats:**

• 👤 Total Users: `{total_users}`
• 🆕 New Users (24h): `{new_users}`
• 💬 Total Chats: `{total_chats}`
• 🆕 New Chats (24h): `{new_chats}`"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Close", callback_data="close_stats")]
    ])

    await message.reply_text(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, query: CallbackQuery):
    await query.message.delete()
