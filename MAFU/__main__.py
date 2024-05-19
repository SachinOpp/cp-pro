import asyncio
import importlib
from pyrogram import idle
from MAFU import MAFU
from MAFU.modules import ALL_MODULES

LOGGER_ID = -1002010924139

loop = asyncio.get_event_loop()

async def roy_bot():
    for all_module in ALL_MODULES:
        importlib.import_module("MAFU.modules." + all_module)
    print("♥︎ B𝗈𝗍 Started Successfully.")
    await idle()
    print("♥︎ Don't edit baby, otherwise you get an error. @ALL_SANATANI_BOT")
    await MAFU.send_message(LOGGER_ID, "**✦ ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ.\n\n✦ ᴊᴏɪɴ - @II_4ST_OFFICIAL_II**")

if __name__ == "__main__":
    loop.run_until_complete(roy_bot())




