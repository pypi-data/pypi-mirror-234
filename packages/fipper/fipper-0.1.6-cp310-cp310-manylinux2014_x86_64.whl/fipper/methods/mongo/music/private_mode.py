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


class PrivateMode:
    async def is_private_mode(self: "fipper.Client") -> bool:
        privatemodedb = self.mongo_async.private_mode
        chat = await privatemodedb.find_one({"bot_id": self.me.id})
        if not chat:
            return False
        return chat['mode']


    async def set_private_mode(self: "fipper.Client", mode: Optional[bool]) -> None:
        privatemodedb = self.mongo_async.private_mode
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
            return await privatemodedb.insert_one({"bot_id": self.me.id, "mode": None})
