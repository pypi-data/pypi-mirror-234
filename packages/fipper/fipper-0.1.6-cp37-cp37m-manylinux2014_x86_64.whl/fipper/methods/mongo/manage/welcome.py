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


class Welcome:
    async def is_welcome(self: "fipper.Client", chat_id: int) -> bool:
        welcomedb = self.mongo_async.welcome
        axd = await welcomedb.find_one({"chat_id": chat_id})
        if axd:
            try:
                return axd["welcome"]
            except KeyError:
                return False
        else:
            return False
    
    
    async def welcome(self: "fipper.Client", chat_id: int, welcome: Optional[bool]) -> None:
        welcomedb = self.mongo_async.welcome
        is_antiservice = await welcomedb.find_one({"chat_id": chat_id})
        if welcome:
            if is_antiservice:
                return
            else:
                return await welcomedb.insert_one({"chat_id": chat_id, "welcome": welcome})
        else:
            return await welcomedb.update_one({"chat_id": chat_id, "welcome": False})


    async def get_welcome(self: "fipper.Client", chat_id: int) -> str:
        welcomedb = self.mongo_async.welcome
        axd = await welcomedb.find_one({"chat_id": chat_id})
        if axd:
            try:
                return axd["text"]
            except KeyError:
                return None
        else:
            return None


    async def set_welcome(self: "fipper.Client", chat_id: int, text: str):
        welcomedb = self.mongo_async.welcome
        axd = await welcomedb.find_one({"chat_id": chat_id})
        if axd:
            if text:
                return await welcomedb.update_one(
                    {"chat_id": chat_id}, {"$set": {"text": text}}, upsert=True
                )
            else:
                return await welcomedb.update_one(
                    {"chat_id": chat_id},
                    {
                        "$set": {"text": "Hai {first_name}\n\nSelamat Bergabung Di {title}"}}, upsert=True
                )
        else:
            if text:
                return await welcomedb.insert_one(
                    {"chat_id": chat_id, "text": text}, upsert=True
                )
            else:
                return await welcomedb.insert_one(
                    {"chat_id": chat_id, "text": "Hai {first_name}\n\nSelamat Bergabung Di {title}"}, upsert=True
                )
