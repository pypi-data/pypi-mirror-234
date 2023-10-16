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


class BotAdmin:
    async def bot_admin(self: "fipper.Client", chat_id, title):
        botadmindb = self.mongo_async.botadmin
        cek = await botadmindb.find_one({"bot_id": self.me.id, "chat_id": chat_id})
        if cek:
            await botadmindb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "chat_id": chat_id,
                        "title": title,
                    }
                },
            )
        else:
            await botadmindb.insert_one({"bot_id": self.me.id, "chat_id": chat_id, "title": title})


    async def bot_nonadmin(self: "fipper.Client", chat_id):
        botadmindb = self.mongo_async.botadmin
        await botadmindb.delete_one({"bot_id": self.me.id, "chat_id": chat_id})


    async def get_bot_admin(self: "fipper.Client"):
        botadmindb = self.mongo_async.botadmin
        r = [jo async for jo in botadmindb.find({"bot_id": self.me.id})]
        if r:
            return r
        else:
            return False
