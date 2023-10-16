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

from typing import Union

import fipper


class AutoLeaveAssistant:
    async def get_leave_assistant(self: "fipper.Client"):
        autoleavedb = self.mongo_async.leave_assistant
        chat = await autoleavedb.find_one({"bot_id": self.me.id})
        if not chat:
            return False
        return chat['mode']


    async def get_leave_assistant_time(self: "fipper.Client"):
        autoleavedb = self.mongo_async.leave_assistant
        chat = await autoleavedb.find_one({"bot_id": self.me.id})
        if not chat:
            return 5
        return chat['time']


    async def set_leave_assistant(self: "fipper.Client", mode: bool = None, time: int = None):
        autoleavedb = self.mongo_async.leave_assistant
        is_antiservice = await autoleavedb.find_one({"bot_id": self.me.id})
        if mode:
            if is_antiservice:
                await autoleavedb.update_one(
                    {"bot_id": self.me.id},
                    {
                        "$set": {
                            "mode": mode,
                            "time": time
                        }
                    }
                )
            else:
                return await autoleavedb.insert_one({"bot_id": self.me.id, "mode": mode, "time": time})
        else:
            if is_antiservice:
                await autoleavedb.update_one(
                    {"bot_id": self.me.id},
                    {
                        "$set": {
                            "mode": False,
                            "time": 30
                        }
                    }
                )
            else:
                return await autoleavedb.insert_one({"bot_id": self.me.id, "mode": False, "time": 30})
