import motor, asyncio
import motor.motor_asyncio
import pymongo, os
from config import DB_URI, DB_NAME
import logging
from datetime import datetime

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

logging.basicConfig(level=logging.INFO)

class SS_BOTZ:

    def __init__(self, DB_URI, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.database = self.dbclient[DB_NAME]

        # Admin collection
        self.admins_data = self.database['admins']

        # ✅ Added new collections for uptime system
        self.uptime_bots = self.database['uptime_bots']
        self.uptime_logs = self.database['uptime_logs']

    # ===================[ ADMIN DATA ]=================== #
    async def admin_exist(self, admin_id: int):
        found = await self.admins_data.find_one({'_id': admin_id})
        return bool(found)

    async def add_admin(self, admin_id: int):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({'_id': admin_id})
            return

    async def del_admin(self, admin_id: int):
        if await self.admin_exist(admin_id):
            await self.admins_data.delete_one({'_id': admin_id})
            return

    async def get_all_admins(self):
        users_docs = await self.admins_data.find().to_list(length=None)
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids

    # ----------------------------------------------------
    async def add_bot_for_uptime(self, username, webhook, interval, owner_id):
        """Add or replace a bot for uptime monitoring (per username)"""
        data = {
            "_id": username.lower(),  # use username as unique key
            "username": username,
            "webhook": webhook,
            "interval": interval,
            "owner_id": owner_id,
            "is_online": None,
            "last_checked": None,
            "status_msg": None
        }
        await self.uptime_bots.replace_one({"_id": username.lower()}, data, upsert=True)
        return True

    # ----------------------------------------------------
    async def get_uptime_bot(self, username, owner_id):
        """Get a specific monitored bot (username + owner verify)"""
        return await self.uptime_bots.find_one({"_id": username.lower(), "owner_id": owner_id})

    # ----------------------------------------------------
    async def remove_uptime_bot(self, username, owner_id):
        """Remove monitored bot (only if owner matches)"""
        result = await self.uptime_bots.delete_one({"_id": username.lower(), "owner_id": owner_id})
        return result.deleted_count > 0

    # ----------------------------------------------------
    async def update_uptime_status(self, username, is_online, msg):
        """Update current bot status"""
        await self.uptime_bots.update_one(
            {"_id": username.lower()},
            {"$set": {
                "is_online": is_online,
                "last_checked": datetime.now(),
                "status_msg": msg
            }}
        )
# ----------------- Initialize DB -----------------
db = SS_BOTZ(DB_URI, DB_NAME)
