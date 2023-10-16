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


class FotoMenfes:
    async def add_foto_boy(self: "fipper.Client", foto_boy):
        hastagdb = self.mongo_async.foto_boy
        cek = await hastagdb.find_one({"bot_id": self.me.id, "foto_boy": foto_boy})
        if cek:
            await hastagdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "foto_boy": foto_boy,
                    }
                },
            )
        else:
            await hastagdb.insert_one({"bot_id": self.me.id, "foto_boy": foto_boy})


    async def del_foto_boy(self: "fipper.Client", foto_boy):
        hastagdb = self.mongo_async.foto_boy
        await hastagdb.delete_one({"bot_id": self.me.id, "foto_boy": foto_boy})


    async def get_foto_boy(self: "fipper.Client"):
        hastagdb = self.mongo_async.foto_boy
        r = await hastagdb.find_one({"bot_id": self.me.id})
        if r:
            return r['foto_boy']
        else:
            return None


    async def add_foto_girl(self: "fipper.Client", foto_girl):
        hastagdb = self.mongo_async.foto_girl
        cek = await hastagdb.find_one({"bot_id": self.me.id, "foto_girl": foto_girl})
        if cek:
            await hastagdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "foto_girl": foto_girl,
                    }
                },
            )
        else:
            await hastagdb.insert_one({"bot_id": self.me.id, "foto_girl": foto_girl})


    async def del_foto_boy(self: "fipper.Client", foto_girl):
        hastagdb = self.mongo_async.foto_girl
        await hastagdb.delete_one({"bot_id": self.me.id, "foto_girl": foto_girl})


    async def get_foto_boy(self: "fipper.Client"):
        hastagdb = self.mongo_async.foto_girl
        r = await hastagdb.find_one({"bot_id": self.me.id})
        if r:
            return r['foto_girl']
        else:
            return None
