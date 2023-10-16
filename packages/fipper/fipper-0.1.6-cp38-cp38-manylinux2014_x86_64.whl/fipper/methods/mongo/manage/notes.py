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


class Notes:
    async def add_note(self: "fipper.Client", chat_id, trigger, raw_data, file_id, note_type):
        notedb = self.mongo_async.notes
        cek = await notedb.find_one({"chat_id": chat_id, "trigger": trigger})
        if cek:
            await notedb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "trigger": trigger,
                        "raw_data": raw_data,
                        "file_id": file_id,
                        "note_type": note_type
                    }
                },
            )
        else:
            await notedb.insert_one(
                {
                    "chat_id": chat_id,
                    "trigger": trigger,
                    "raw_data": raw_data,
                    "file_id": file_id,
                    "note_type": note_type,
                }
            )


    async def del_note(self: "fipper.Client", chat_id, trigger):
        notedb = self.mongo_async.notes
        await notedb.delete_one({"chat_id": chat_id, "trigger": trigger})


    async def get_all_notes(self: "fipper.Client", chat_id):
        notedb = self.mongo_async.notes
        r = [jo async for jo in notedb.find({"chat_id": chat_id})]
        if r:
            return r
        else:
            return False
