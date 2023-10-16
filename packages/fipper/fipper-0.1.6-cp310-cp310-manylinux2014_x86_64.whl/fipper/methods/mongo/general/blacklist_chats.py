import fipper


class BlacklistedChats:
    async def get_blacklist_chats(self: 'fipper.Client') -> list:
        blacklist_chatdb = self.mongo_async.blacklistChat
        sudo = await blacklist_chatdb.find_one({"bot_id": self.me.id})
        if not sudo:
            return []
        return sudo['blacklist_chat']


    async def add_blacklist_chats(self: 'fipper.Client', chat_id: int) -> bool:
        blacklist_chatdb = self.mongo_async.blacklistChat
        blacklist_chat = await self.get_blacklist_chats()
        blacklist_chat.append(chat_id)
        await blacklist_chatdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"blacklist_chat": blacklist_chat}}, upsert=True
        )
        return True


    async def del_blacklist_chats(self: 'fipper.Client', chat_id: int) -> bool:
        blacklist_chatdb = self.mongo_async.blacklistChat
        blacklist_chat = await self.get_blacklist_chats()
        blacklist_chat.remove(chat_id)
        await blacklist_chatdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"blacklist_chat": blacklist_chat}}, upsert=True
        )
        return True
