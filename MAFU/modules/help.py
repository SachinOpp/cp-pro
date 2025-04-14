from pyrogram import filters, filters
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from MAFU import MAFU as app

# HELP TEXTS
HELP_1 = "Help Section 1"
HELP_2 = "Help Section 2"
HELP_3 = "Help Section 3"
HELP_4 = "Help Section 4"
HELP_5 = "Help Section 5"
HELP_6 = "Help Section 6"
HELP_7 = "Help Section 7"
HELP_8 = "Help Section 8"
HELP_9 = "Help Section 9"
HELP_10 = "Help Section 10"
HELP_11 = "Help Section 11"
HELP_12 = "Help Section 12"
HELP_13 = "Help Section 13"
HELP_14 = "Help Section 14"
HELP_15 = "Help Section 15"

HELPABLE = {
    "hb1": HELP_1, "hb2": HELP_2, "hb3": HELP_3, "hb4": HELP_4, "hb5": HELP_5,
    "hb6": HELP_6, "hb7": HELP_7, "hb8": HELP_8, "hb9": HELP_9, "hb10": HELP_10,
    "hb11": HELP_11, "hb12": HELP_12, "hb13": HELP_13, "hb14": HELP_14, "hb15": HELP_15
}


def private_help_panel():
    return [
        [InlineKeyboardButton("1", callback_data="help_callback hb1"),
         InlineKeyboardButton("2", callback_data="help_callback hb2"),
         InlineKeyboardButton("3", callback_data="help_callback hb3"),
         InlineKeyboardButton("4", callback_data="help_callback hb4"),
         InlineKeyboardButton("5", callback_data="help_callback hb5")],
        [InlineKeyboardButton("6", callback_data="help_callback hb6"),
         InlineKeyboardButton("7", callback_data="help_callback hb7"),
         InlineKeyboardButton("8", callback_data="help_callback hb8"),
         InlineKeyboardButton("9", callback_data="help_callback hb9"),
         InlineKeyboardButton("10", callback_data="help_callback hb10")],
        [InlineKeyboardButton("11", callback_data="help_callback hb11"),
         InlineKeyboardButton("12", callback_data="help_callback hb12"),
         InlineKeyboardButton("13", callback_data="help_callback hb13"),
         InlineKeyboardButton("14", callback_data="help_callback hb14"),
         InlineKeyboardButton("15", callback_data="help_callback hb15")],
        [InlineKeyboardButton("Close", callback_data="help_close")]
    ]


def help_back_markup():
    return InlineKeyboardMarkup(private_help_panel())


@app.on_message(filters.command(["help"]))
async def help_com_group(client, message: Message):
    await message.reply_text(
        "नीचे दिए गए बटनों से सहायता जानकारी देखें:",
        reply_markup=help_back_markup()
    )


@app.on_callback_query(filters.regex("help_callback"))
async def helper_cb(client, callback_query: CallbackQuery):
    cb = callback_query.data.strip().split(None, 1)[1]
    if cb in HELPABLE:
        await callback_query.edit_message_text(
            HELPABLE[cb],
            reply_markup=help_back_markup(),
            disable_web_page_preview=True
        )
        await callback_query.answer()


@app.on_callback_query(filters.regex("help_close"))
async def close_help_cb(client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer("Closed Help", show_alert=False)
