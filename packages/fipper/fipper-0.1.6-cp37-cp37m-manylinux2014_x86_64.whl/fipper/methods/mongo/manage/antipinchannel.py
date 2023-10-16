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


class AntiPinChannel:
    async def is_antipinchannel(self: "fipper.Client", chat_id: int) -> bool:
        antipindb = self.mongo_async.antipinchannel
        chat = await antipindb.find_one({"chat_id": chat_id})
        if not chat:
            return
        return chat['antipin']


    async def antipinchannel(self: "fipper.Client", chat_id: int, antipin: Optional[bool]) -> None:
        antipindb = self.mongo_async.antipinchannel
        is_antiservice = await antipindb.find_one({"chat_id": chat_id})
        if antipin:
            if is_antiservice:
                return
            else:
                return await antipindb.insert_one({"chat_id": chat_id, "antipin": antipin})
        else:
            return await antipindb.insert_one({"chat_id": chat_id, "antipin": None})
