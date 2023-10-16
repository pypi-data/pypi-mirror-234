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


class Admins:
    async def get_admin(self: "fipper.Client", chat_id: int):
        adminsdb = self.mongo_async.admins
        admin = await adminsdb.find_one({"chat_id": chat_id})
        if not admin:
            return []
        return admin['listadmin']

    async def add_admin(self: "fipper.Client", chat_id: int, user_id: int) -> bool:
        adminsdb = self.mongo_async.admins
        listadmin = await self.get_admin(chat_id)
        listadmin.append(user_id)
        await adminsdb.update_one(
            {"chat_id": chat_id}, {"$set": {"listadmin": listadmin}}, upsert=True
        )
        return True

    async def del_admin(self: "fipper.Client", chat_id: int, user_id: int) -> bool:
        adminsdb = self.mongo_async.admins
        listadmin = await self.get_admin(chat_id)
        listadmin.remove(user_id)
        await adminsdb.update_one(
            {"chat_id": chat_id}, {"$set": {"listadmin": listadmin}}, upsert=True
        )
        return True

    async def del_all_admin(self: "fipper.Client", chat_id: int) -> bool:
        adminsdb = self.mongo_async.admins
        listadmin = await self.get_admin(chat_id)
        listadmin.clear()
        await adminsdb.update_one(
            {"chat_id": chat_id}, {"$set": {"listadmin": listadmin}}, upsert=True
        )
        return True
