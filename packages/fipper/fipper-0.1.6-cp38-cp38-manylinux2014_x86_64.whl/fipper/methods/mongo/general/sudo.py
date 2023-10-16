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


class Sudoers:
    async def get_sudo(self: "fipper.Client") -> list:
        sudoersdb = self.mongo_async.sudoers
        sudo = await sudoersdb.find_one({"bot_id": self.me.id})
        if not sudo:
            return []
        return sudo['sudoers']

    async def add_sudo(self: "fipper.Client", user_id: int) -> bool:
        sudoersdb = self.mongo_async.sudoers
        sudoers = await self.get_sudo()
        sudoers.append(user_id)
        await sudoersdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"sudoers": sudoers}}, upsert=True
        )
        return True


    async def del_sudo(self: "fipper.Client", user_id: int) -> bool:
        sudoersdb = self.mongo_async.sudoers
        sudoers = await self.get_sudo()
        sudoers.remove(user_id)
        await sudoersdb.update_one(
            {"bot_id": self.me.id}, {"$set": {"sudoers": sudoers}}, upsert=True
        )
        return True
