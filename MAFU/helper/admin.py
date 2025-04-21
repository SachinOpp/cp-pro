from typing import Callable, Union
from functools import wraps
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, CallbackQuery

from MAFU import MAFU as app
from config import OWNER_ID

# Function to check admin status
async def is_admins_check(chat_id: int, user_id: int) -> bool:
    if user_id == OWNER_ID:
        return True
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"[is_admins_check Error] chat_id={chat_id}, user_id={user_id} => {e}")
        return False

# Decorator to restrict access to admins only
def is_admins(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(c: Client, m: Union[Message, CallbackQuery]):
        try:
            if isinstance(m, CallbackQuery):
                user_id = m.from_user.id
                chat_id = m.message.chat.id
            elif isinstance(m, Message):
                user_id = m.from_user.id
                chat_id = m.chat.id
            else:
                print(f"[is_admins Error] Unsupported type: {type(m)}")
                return

            if user_id == OWNER_ID or await is_admins_check(chat_id, user_id):
                return await func(c, m)
            else:
                msg = "Only is admins can use this!"
                if isinstance(m, CallbackQuery):
                    try:
                        await m.answer(msg, show_alert=True)
                    except:
                        await m.message.reply_text(msg)
                else:
                    await m.reply_text(msg)
        except Exception as e:
            print(f"[is_admins Error] {e}")
    return wrapper
