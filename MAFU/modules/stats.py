from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from MAFU.helper.database import get_users, get_chats, get_new_users, get_new_chats
from MAFU import MAFU as app


@app.on_message(filters.command("stats") & filters.private)
async def stats_handler(client: Client, message: Message):
    total_users = len((await get_users())["users"])
    total_chats = len((await get_chats())["chats"])

    new_users = await get_new_users()
    new_chats = await get_new_chats()

    text = (
        "**Bot Stats:**\n\n"
        f"**Total Users:** {total_users}\n"
        f"**Total Chats:** {total_chats}\n\n"
        f"**New Users (24hrs):** {new_users}\n"
        f"**New Chats (24hrs):** {new_chats}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Close", callback_data="close")]
    ])

    await message.reply_text(text, reply_markup=keyboard)
