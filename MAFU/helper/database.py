import datetime
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)

# Database Collections
authdb = mongo.auth.authusers
users_collection = mongo.users.users
chats_collection = mongo.chats.chatsdb
sudodb = mongo.sudo.sudousers
settings_collection = mongo.settings.settings  # Explicitly define settings

# ──────────────────────────────── AUTH USERS ────────────────────────────────

async def add_auth(chat_id: int, user_id: int):
    if await is_auth(chat_id, user_id):
        return
    await authdb.insert_one({"chat_id": chat_id, "user_id": user_id})

async def remove_auth(chat_id: int, user_id: int):
    if not await is_auth(chat_id, user_id):
        return
    await authdb.delete_one({"chat_id": chat_id, "user_id": user_id})

async def is_auth(chat_id: int, user_id: int) -> bool:
    return bool(await authdb.find_one({"chat_id": chat_id, "user_id": user_id}))

async def get_auth_users(chat_id: int) -> dict:
    auth_users = []
    async for user in authdb.find({"chat_id": chat_id}):
        auth_users.append(user["user_id"])
    return {"auth_users": auth_users}

# ──────────────────────────────── USERS ────────────────────────────────

async def get_users():
    user_list = []
    async for user in users_collection.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    return {"users": user_list}

async def get_user(user):
    data = await get_users()
    return user in data["users"]

async def add_user(user):
    if await get_user(user):
        return
    await users_collection.insert_one({
        "user": user,
        "joined_at": datetime.datetime.utcnow()
    })

async def del_user(user):
    if not await get_user(user):
        return
    await users_collection.delete_one({"user": user})

async def get_new_users():
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    return await users_collection.count_documents({"joined_at": {"$gte": one_day_ago}})

# ──────────────────────────────── CHATS ────────────────────────────────

async def get_chats():
    chat_list = []
    async for chat in chats_collection.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    return {"chats": chat_list}

async def get_chat(chat):
    data = await get_chats()
    return chat in data["chats"]

async def add_chat(chat):
    if await get_chat(chat):
        return
    await chats_collection.insert_one({
        "chat": chat,
        "joined_at": datetime.datetime.utcnow()
    })

async def del_chat(chat):
    if not await get_chat(chat):
        return
    await chats_collection.delete_one({"chat": chat})

async def get_new_chats():
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    return await chats_collection.count_documents({"joined_at": {"$gte": one_day_ago}})

# ──────────────────────────────── SETTINGS ────────────────────────────────

async def get_settings(chat_id):
    settings = await settings_collection.find_one({"chat_id": chat_id})
    return settings or {}

async def save_settings(chat_id, key, value):
    await settings_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {key: value}},
        upsert=True
    )

# ──────────────────────────────── SUDO USERS ────────────────────────────────

async def add_sudo(user_id: int):
    if await is_sudo(user_id):
        return
    await sudodb.insert_one({"user_id": user_id})

async def remove_sudo(user_id: int):
    if not await is_sudo(user_id):
        return
    await sudodb.delete_one({"user_id": user_id})

async def is_sudo(user_id: int) -> bool:
    return bool(await sudodb.find_one({"user_id": user_id}))

async def get_sudoers() -> list:
    sudo_list = []
    async for user in sudodb.find({}):
        sudo_list.append(user["user_id"])
    return sudo_list
