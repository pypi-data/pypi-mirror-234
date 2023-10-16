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

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


class MongoDB:
    def __init__(self, mongo_db):
        try:
            self._mongo_async_ = AsyncIOMotorClient(mongo_db)
            self._mongo_sync_ = MongoClient(mongo_db)
        except AttributeError:
            return

    def mongo_async(self):
        return self._mongo_async_.Fipper
    
    def mongo_sync(self):
        return self._mongo_sync_.Fipper
