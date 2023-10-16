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


class OwnerBot:
    def set_owner(self: "fipper.Client", owner: int):
        hndlrdb = self.mongo_sync.owner
        cek = hndlrdb.find_one({"bot_id": self.me.id})
        if cek:
            hndlrdb.update_one({"bot_id": self.me.id}, {"$set": {"owner": owner}})
        else:
            hndlrdb.insert_one(
                {
                    "bot_id": self.me.id,
                    "owner": owner
                }
            )

    def get_owner(self: "fipper.Client"):
        hndlrdb = self.mongo_sync.owner
        x = hndlrdb.find_one({'bot_id': self.me.id})
        if not x:
            return None
        return x['owner']
