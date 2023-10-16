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


class ChatSupport:
    # Channel SUipport
    async def channel_support(self: 'fipper.Client'):
        active_voice_db = self.mongo_async.channel_support
        aktif = await active_voice_db.find_one({"bot_id": self.me.id})
        if not aktif:
            return None
        return aktif['support']

    async def add_channel_support(self: 'fipper.Client', chat_link: str):
        active_voice_db = self.mongo_async.channel_support
        await active_voice_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"support": chat_link}}, upsert=True
        )
        return True

    async def del_channel_support(self: 'fipper.Client', chat_link: str):
        active_voice_db = self.mongo_async.channel_support
        await active_voice_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"support": chat_link}}, upsert=True
        )
        return True


    # Group Chat Support
    async def group_support(self: 'fipper.Client'):
        active_video_db = self.mongo_async.group_support
        aktif = await active_video_db.find_one({"bot_id": self.me.id})
        if not aktif:
            return None
        return aktif['support']

    async def add_group_support(self: 'fipper.Client', chat_link: str):
        active_video_db = self.mongo_async.group_support
        await active_video_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"support": chat_link}}, upsert=True
        )
        return True

    async def del_group_support(self: 'fipper.Client', chat_link: str):
        active_video_db = self.mongo_async.group_support
        await active_video_db.update_one(
            {"bot_id": self.me.id}, {"$set": {"support": chat_link}}, upsert=True
        )
        return True
