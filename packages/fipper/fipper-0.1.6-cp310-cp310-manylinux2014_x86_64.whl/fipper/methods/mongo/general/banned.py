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


class Banned:
    async def add_banned(self: "fipper.Client", chat_id, user, nama):
        banneddb = self.mongo_async.banned
        cek = await banneddb.find_one({"chat_id": chat_id, "user": user})
        if cek:
            await banneddb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "user": user,
                        "nama": nama,
                    }
                },
            )
        else:
            await banneddb.insert_one({"chat_id": chat_id, "user": user, "nama": nama})


    async def del_banned(self: "fipper.Client", chat_id, user):
        banneddb = self.mongo_async.banned
        await banneddb.delete_one({"chat_id": chat_id, "user": user})


    async def get_all_banned(self: "fipper.Client", chat_id):
        banneddb = self.mongo_async.banned
        r = [jo async for jo in banneddb.find({"chat_id": chat_id})]
        if r:
            return r
        else:
            return False
