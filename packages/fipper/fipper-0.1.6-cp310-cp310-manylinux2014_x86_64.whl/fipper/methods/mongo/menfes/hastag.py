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


class HasTag:
    async def add_tag(self: "fipper.Client", hastag):
        hastagdb = self.mongo_async.hastag
        cek = await hastagdb.find_one({"bot_id": self.me.id, "hastag": hastag})
        if cek:
            await hastagdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "hastag": hastag,
                    }
                },
            )
        else:
            await hastagdb.insert_one({"bot_id": self.me.id, "hastag": hastag})


    async def del_tag(self: "fipper.Client", hastag):
        hastagdb = self.mongo_async.hastag
        await hastagdb.delete_one({"bot_id": self.me.id, "hastag": hastag})


    async def get_tag(self: "fipper.Client"):
        hastagdb = self.mongo_async.hastag
        r = await hastagdb.find_one({"bot_id": self.me.id})
        if r:
            return r['hastag']
        else:
            return None
