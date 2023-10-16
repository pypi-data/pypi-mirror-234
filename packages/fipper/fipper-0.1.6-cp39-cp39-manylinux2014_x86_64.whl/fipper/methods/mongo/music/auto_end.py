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

from typing import Optional

import fipper


class AutoEnd:
    async def is_autoend(self: "fipper.Client") -> bool:
        privatemodedb = self.mongo_async.auto_end
        chat = await privatemodedb.find_one({"bot_id": self.me.id})
        if not chat:
            return False
        return chat['mode']


    async def set_autoend(self: "fipper.Client", mode: bool = None):
        privatemodedb = self.mongo_async.auto_end
        is_antiservice = await privatemodedb.find_one({"bot_id": self.me.id})
        if mode:
            if is_antiservice:
                await privatemodedb.update_one(
                    {"bot_id": self.me.id},
                    {
                        "$set": {
                            "mode": mode
                        }
                    }
                )
            else:
                return await privatemodedb.insert_one({"bot_id": self.me.id, "mode": mode})
        else:
            if is_antiservice:
                await privatemodedb.update_one(
                    {"bot_id": self.me.id},
                    {
                        "$set": {
                            "mode": False
                        }
                    }
                )
            else:
                return await privatemodedb.insert_one({"bot_id": self.me.id, "mode": False})
