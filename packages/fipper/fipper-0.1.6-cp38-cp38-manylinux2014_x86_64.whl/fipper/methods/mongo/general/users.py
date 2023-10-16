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


class UserDB:
    async def cek_user(self: "fipper.Client") -> list:
        userdb = self.mongo_async.broad
        sudo = await userdb.find_one({"bot_id": self.me.id})
        if not sudo:
            return []
        return sudo['user']

    async def add_user(self: "fipper.Client", user_id: int) -> bool:
        userdb = self.mongo_async.broad
        users = await self.cek_user()
        users.append(user_id)
        await userdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"user": users}}, upsert=True
        )
        return True

    async def del_user(self: "fipper.Client", user_id: int) -> bool:
        userdb = self.mongo_async.broad
        users = await self.cek_user()
        users.remove(user_id)
        await userdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"user": users}}, upsert=True
        )
        return True
