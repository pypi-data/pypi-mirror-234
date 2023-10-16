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

from typing import Optional, Tuple

import fipper


class Warn:
    async def get_warn_action(self: "fipper.Client", chat_id: int) -> Tuple[Optional[str], bool]:
        warndb = self.mongo_async.warn
        res = await warndb.find_one({"chat_id": chat_id})
        if res:
            try:
                aksi = res['action']
                return aksi
            except KeyError:
                return "mute"
        else:
            return "mute"


    async def set_warn_action(self: "fipper.Client", chat_id: int, action: Optional[str]):
        warndb = self.mongo_async.warn
        cek = await warndb.find_one({"chat_id": chat_id, "action": action})
        if cek:
            await warndb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "action": action,
                    },
                }
            )
        else:
            await warndb.insert_one(
                {
                    "chat_id": chat_id,
                    "action": action,
                }
            )


    async def get_warns(self: "fipper.Client", chat_id, user_id):
        warndb = self.mongo_async.warn
        r = await warndb.find_one({"chat_id": chat_id, "user_id": user_id})
        if r:
            try:
                num = r['number']
                return num
            except KeyError:
                return 0
        else:
            return 0


    async def add_warns(self: "fipper.Client", chat_id, user_id, number):
        warndb = self.mongo_async.warn
        cek = await warndb.find_one({"chat_id": chat_id, "user_id": user_id})
        if cek:
            await warndb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "number": number,
                    },
                }
            )
        else:
            await warndb.insert_one(
                {
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "number": number,
                }
            )

    async def reset_warns(self: "fipper.Client", chat_id, user_id):
        warndb = self.mongo_async.warn
        res = await warndb.find_one({"chat_id": chat_id, "user_id": user_id})
        if res:
            await warndb.delete_one({"user_id": user_id})


    async def get_warns_limit(self: "fipper.Client", chat_id):
        warndb = self.mongo_async.warn
        res = await warndb.find_one({"chat_id": chat_id})
        if res:
            try:
                limit = res['warns_limit']
                return limit
            except KeyError:
                return 3
        else:
            return 3


    async def set_warns_limit(self: "fipper.Client", chat_id, warns_limit):
        warndb = self.mongo_async.warn
        cek = await warndb.find_one({"chat_id": chat_id, "warns_limit": warns_limit})
        if cek:
            await warndb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "warns_limit": warns_limit,
                    },
                }
            )
        else:
            await warndb.insert_one(
                {
                    "chat_id": chat_id,
                    "warns_limit": warns_limit,
                }
            )


    async def all_warns(self: "fipper.Client", chat_id):
        warndb = self.mongo_async.warn
        r = [jo async for jo in warndb.find({"chat_id": chat_id})]
        if r:
            return r
        else:
            return []
