


import fipper


class ServedChat:
    async def get_served_chat(self: 'fipper.Client') -> list:
        chatsdb = self.mongo_async.chats
        sudo = await chatsdb.find_one({"bot_id": self.me.id})
        if not sudo:
            return []
        return sudo['served_chat']

    async def add_served_chat(self: 'fipper.Client', chat_id: int):
        chatsdb = self.mongo_async.chats
        served_chat = await self.get_served_chat()
        served_chat.append(chat_id)
        await chatsdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"served_chat": served_chat}}, upsert=True
        )
        return True

    async def del_served_chat(self: 'fipper.Client', chat_id: int) -> bool:
        chatsdb = self.mongo_async.chats
        served_chat = await self.get_served_chat()
        served_chat.remove(chat_id)
        await chatsdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"served_chat": served_chat}}, upsert=True
        )
        return True
