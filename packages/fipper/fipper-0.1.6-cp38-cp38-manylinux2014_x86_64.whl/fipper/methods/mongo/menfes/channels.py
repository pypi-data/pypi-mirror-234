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


class Channels:
    async def add_channel(self: "fipper.Client", chat_id):
        channeldb = self.mongo_async.channel
        cek = await channeldb.find_one({"bot_id": self.me.id, "chat_id": chat_id})
        if cek:
            await channeldb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "chat_id": chat_id,
                    }
                },
            )
        else:
            await channeldb.insert_one({"bot_id": self.me.id, "chat_id": chat_id})


    async def del_channel(self: "fipper.Client", chat_id):
        channeldb = self.mongo_async.channel
        await channeldb.delete_one({"bot_id": self.me.id, "chat_id": chat_id})


    async def get_channel(self: "fipper.Client"):
        channeldb = self.mongo_async.channel
        r = await channeldb.find_one({"bot_id": self.me.id})
        if r:
            return r['chat_id']
        else:
            return None
