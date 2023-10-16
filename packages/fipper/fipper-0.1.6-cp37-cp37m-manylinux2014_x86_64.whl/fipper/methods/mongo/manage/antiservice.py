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


class AntiService:
    async def is_antiservice(self: "fipper.Client", chat_id: int) -> bool:
        antiservicedb = self.mongo_async.antiservice
        chat = await antiservicedb.find_one({"chat_id": chat_id})
        if not chat:
            return
        return chat['service']


    async def antiservice(self: "fipper.Client", chat_id: int, service: Optional[bool]) -> None:
        antiservicedb = self.mongo_async.antiservice
        is_antiservice = await antiservicedb.find_one({"chat_id": chat_id})
        if service:
            if is_antiservice:
                return
            else:
                return await antiservicedb.insert_one({"chat_id": chat_id, "service": service})
        else:
            return await antiservicedb.insert_one({"chat_id": chat_id, "service": None})
