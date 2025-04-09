"""from . import sudodb

async def add_sudo(user_id: int):
    """
    Add a user to sudoers.
    """
    if not await sudodb.find_one({"user_id": user_id}):
        await sudodb.insert_one({"user_id": user_id})

async def remove_sudo(user_id: int):
    """
    Remove a user from sudoers.
    """
    await sudodb.delete_one({"user_id": user_id})

async def get_sudoers() -> list:
    """
    Get a list of all sudo users.
    """
    sudoers = []
    async for user in sudodb.find({}):
        sudoers.append(user["user_id"])
    return sudoers

async def is_sudo(user_id: int) -> bool:
    """
    Check if a user is in sudo list.
    """
    return bool(await sudodb.find_one({"user_id": user_id}))
    """
#=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×=×

import datetime
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
sudodb = mongo.sudo.sudoers  # You can change this collection name as you prefer

# SUDO FUNCTIONS

async def get_sudoers():
    sudo_list = []
    async for user in sudodb.find({}):
        sudo_list.append(user["user_id"])
    return {"sudoers": sudo_list}

async def is_sudo(user_id: int):
    data = await get_sudoers()
    return user_id in data["sudoers"]

async def add_sudo(user_id: int):
    if await is_sudo(user_id):
        return
    await sudodb.insert_one({
        "user_id": user_id,
        "added_at": datetime.datetime.utcnow()
    })

async def remove_sudo(user_id: int):
    if not await is_sudo(user_id):
        return
    await sudodb.delete_one({"user_id": user_id})

async def get_new_sudoers():
    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    return await sudodb.count_documents({"added_at": {"$gte": one_day_ago}})
