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


class SkipPause:
    # Pause-Skip
    async def is_music_playing(self: 'fipper.Client', chat_id: int) -> bool:
        skip_pause_db = self.mongo_async.skip_pause
        mode = await skip_pause_db.find_one({"chat_id": chat_id})
        if not mode:
            return False
        return mode['mode']


    async def music_on(self: 'fipper.Client', chat_id: int):
        skip_pause_db = self.mongo_async.skip_pause
        mode = await skip_pause_db.find_one({"chat_id": chat_id})
        if mode:
            await skip_pause_db.update_one(
                {"chat_id": chat_id}, {"$set": {"mode": True}}, upsert=True
            )
        else:
            await skip_pause_db.insert_one({'chat_id': chat_id, 'mode': True})


    async def music_off(self: 'fipper.Client', chat_id: int):
        skip_pause_db = self.mongo_async.skip_pause
        mode = await skip_pause_db.find_one({"chat_id": chat_id})
        if mode:
            await skip_pause_db.update_one(
                {"chat_id": chat_id}, {"$set": {"mode": False}}, upsert=True
            )
