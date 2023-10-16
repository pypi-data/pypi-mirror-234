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


class Coin:
    async def cek_coin(self: "fipper.Client", user_id):
        coindb = self.mongo_async.coins
        r = await coindb.find_one({"user_id": user_id})
        if r:
            return True
        else:
            return False

    async def add_coin(self: "fipper.Client", user_id, coin):
        coindb = self.mongo_async.coins
        cek = await coindb.find_one({"user_id": user_id})
        if cek:
            await coindb.update_one(
                {"user_id": user_id,},
                {
                    "$set": {
                        "coin": coin,
                    }
                },
            )
        else:
            await coindb.insert_one({"user_id": user_id, "coin": coin})


    async def del_coin(self: "fipper.Client", user_id):
        coindb = self.mongo_async.coins
        await coindb.delete_one({"user_id": user_id})


    async def get_coin(self: "fipper.Client", user_id):
        coindb = self.mongo_async.coins
        r = await coindb.find_one({"user_id": user_id})
        if r:
            return r['coin']
        else:
            return None
