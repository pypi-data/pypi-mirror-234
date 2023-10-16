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


class Ubot:
    def set_ubot(
        self: "fipper.Client", 
        name,
        api_id, 
        api_hash, 
        session_string,
    ):
        ubotdb = self.mongo_sync.ubot
        user = ubotdb.find_one({"bot_id": self.me.id})
        if user:
            ubotdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "name": name,
                        "api_id": api_id,
                        "api_hash": api_hash,
                        "session_string": session_string,
                    }
                },
            )
        else:
            ubotdb.insert_one(
                {
                    "bot_id": self.me.id,
                    "name": name,
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_string": session_string,
                }
            )


    def del_ubot(self: "fipper.Client"):
        ubotdb = self.mongo_sync.ubot
        return ubotdb.delete_one({"bot_id": self.me.id})


    def get_ubot(self: "fipper.Client") -> "fipper.Client":
        ubotdb = self.mongo_sync.ubot
        for bt in ubotdb.find({"bot_id": self.me.id}):
            name = str(bt["name"])
            api_id = bt["api_id"]
            api_hash = bt["api_hash"]
            session_string = bt["session_string"]
            return name, api_id, api_hash, session_string
