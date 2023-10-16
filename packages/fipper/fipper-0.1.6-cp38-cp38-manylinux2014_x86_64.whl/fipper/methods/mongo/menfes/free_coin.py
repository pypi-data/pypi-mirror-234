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


class FreeCoin:
    async def add_free_coin(self: "fipper.Client", user_id, free_coin):
        freecoindb = self.mongo_async.freecoins
        cek = await freecoindb.find_one({"user_id": user_id})
        if cek:
            await freecoindb.update_one(
                {"user_id": user_id,},
                {
                    "$set": {
                        "free_coin": free_coin,
                    }
                },
            )
        else:
            await freecoindb.insert_one({"user_id": user_id, "free_coin": free_coin})


    async def del_free_coin(self: "fipper.Client", user_id):
        freecoindb = self.mongo_async.freecoins
        await freecoindb.delete_one({"user_id": user_id})


    async def get_free_coin(self: "fipper.Client", user_id):
        freecoindb = self.mongo_async.freecoins
        r = await freecoindb.find_one({"user_id": user_id})
        if r:
            return r['free_coin']
        else:
            return None

    async def cek_free_coin(self: "fipper.Client", user_id):
        freecoindb = self.mongo_async.freecoins
        r = await freecoindb.find_one({"user_id": user_id})
        if r:
            return True
        else:
            return False
