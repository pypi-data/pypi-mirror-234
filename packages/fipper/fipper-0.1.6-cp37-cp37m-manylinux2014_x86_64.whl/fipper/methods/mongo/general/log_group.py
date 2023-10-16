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


class LogsGroup:
    async def add_logs(self: "fipper.Client", chat_id):
        logdb = self.mongo_async.log_group
        cek = await logdb.find_one({"bot_id": self.me.id})
        if cek:
            await logdb.update_one(
                {"bot_id": self.me.id,},
                {
                    "$set": {
                        "chat_id": chat_id,
                    }
                },
            )
        else:
            await logdb.insert_one({"bot_id": self.me.id, "chat_id": chat_id})

    async def get_logs(self: "fipper.Client"):
        logdb = self.mongo_async.log_group
        r = await logdb.find_one({"bot_id": self.me.id})
        if not r:
            return None
        return r['chat_id']
