# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import fipper


class ActiveVoiceVideo:
    # Active Voice Chats
    async def get_active_voice_chats(self: 'fipper.Client') -> list:
        active_voice_db = self.mongo_async.active_voice_chat
        aktif = await active_voice_db.find_one({"bot_id": self.me.id})
        if not aktif:
            return []
        return aktif['active_voice']

    async def add_active_voice_chat(self: 'fipper.Client', chat_id: int):
        active_voice_db = self.mongo_async.active_voice_chat
        active_voice = await self.get_active_voice_chats()
        active_voice.append(chat_id)
        await active_voice_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"active_voice": active_voice}}, upsert=True
        )
        return True

    async def remove_active_voice_chat(self: 'fipper.Client', chat_id: int):
        active_voice_db = self.mongo_async.active_voice_chat
        active_voice = await self.get_active_voice_chats()
        active_voice.remove(chat_id)
        await active_voice_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"active_voice": active_voice}}, upsert=True
        )
        return True


    # Active Video Chats
    async def get_active_video_chats(self: 'fipper.Client') -> list:
        active_video_db = self.mongo_async.active_video_chat
        aktif = await active_video_db.find_one({"bot_id": self.me.id})
        if not aktif:
            return []
        return aktif['active_video']

    async def add_active_video_chat(self: 'fipper.Client', chat_id: int):
        active_video_db = self.mongo_async.active_video_chat
        active_video = await self.get_active_video_chats()
        active_video.append(chat_id)
        await active_video_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"active_video": active_video}}, upsert=True
        )
        return True

    async def remove_active_video_chat(self: 'fipper.Client', chat_id: int):
        active_video_db = self.mongo_async.active_video_chat
        active_video = await self.get_active_video_chats()
        active_video.remove(chat_id)
        await active_video_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"active_video": active_video}}, upsert=True
        )
        return True
