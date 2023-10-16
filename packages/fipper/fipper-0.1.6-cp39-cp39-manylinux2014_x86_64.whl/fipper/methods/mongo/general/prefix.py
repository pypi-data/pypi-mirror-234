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

from typing import Union, List

import fipper


class Prefix:
    default_prefix = [".", "!", "*", "^", "-", "?"]

    def set_prefix(self: "fipper.Client", handler: Union[str, List[str]]):
        hndlrdb = self.mongo_sync.prefix
        user_id = self.me.id
        cek = hndlrdb.find_one({"bot_id": user_id})
        if cek:
            hndlrdb.update_one({"bot_id": user_id}, {"$set": {"hndlr": handler.split(' ')}})
        else:
            hndlrdb.insert_one(
                {
                    "bot_id": user_id,
                    "hndlr": handler
                }
            )

    def set_prefix_user(self: "fipper.Client", user_id, handler: Union[str, List[str]]):
        """- For Bot Setting Prefix User Id"""
        hndlrdb = self.mongo_sync.prefix
        cek = hndlrdb.find_one({"user_id": user_id})
        if cek:
            hndlrdb.update_one({"user_id": user_id}, {"$set": {"hndlr": handler}})
        else:
            hndlrdb.insert_one(
                {
                    "user_id": user_id,
                    "hndlr": handler
                }
            )

    def del_prefix(self: "fipper.Client"):
        hndlrdb = self.mongo_sync.prefix
        hndlrdb.update_one({"bot_id": self.me.id}, {"$set": {"hndlr": self.default_prefix}})

    def get_prefix(self: "fipper.Client"):
        hndlrdb = self.mongo_sync.prefix
        x = hndlrdb.find_one({'bot_id': self.me.id})
        if x:
            return x['hndlr']
        else:
            return self.default_prefix

    def get_prefix_user(self: "fipper.Client", user_id):
        hndlrdb = self.mongo_sync.prefix
        x = hndlrdb.find_one({'user_id': user_id})
        if x:
            return x['hndlr']
        else:
            return self.default_prefix
