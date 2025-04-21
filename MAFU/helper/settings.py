from MAFU import mongodb

async def get_settings(chat_id):
    settings = await mongodb.settings.find_one({"chat_id": chat_id})
    return settings or {}

async def save_settings(chat_id, key, value):
    await mongodb.settings.update_one(
        {"chat_id": chat_id},
        {"$set": {key: value}},
        upsert=True
    )
