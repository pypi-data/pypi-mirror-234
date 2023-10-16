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


class Subs:
    async def add_sub_group(self: "fipper.Client", sub_group):
        subsdb = self.mongo_async.subsgroup
        cek = await subsdb.find_one({"bot_id": self.me.id, "sub_group": sub_group})
        if cek:
            await subsdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "sub_group": sub_group,
                    }
                },
            )
        else:
            await subsdb.insert_one({"bot_id": self.me.id, "sub_group": sub_group})


    async def del_sub_group(self: "fipper.Client", sub_group):
        subsdb = self.mongo_async.subsgroup
        await subsdb.delete_one({"bot_id": self.me.id, "sub_group": sub_group})


    async def get_sub_group(self: "fipper.Client"):
        subsdb = self.mongo_async.subsgroup
        r = await subsdb.find_one({"bot_id": self.me.id})
        if r:
            return r['sub_group']
        else:
            return None

    async def add_sub_channel(self: "fipper.Client", sub_channel):
        subsdb = self.mongo_async.subschannel
        cek = await subsdb.find_one({"bot_id": self.me.id, "sub_channel": sub_channel})
        if cek:
            await subsdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "sub_channel": sub_channel,
                    }
                },
            )
        else:
            await subsdb.insert_one({"bot_id": self.me.id, "sub_channel": sub_channel})


    async def del_sub_channel(self: "fipper.Client", sub_channel):
        subsdb = self.mongo_async.subschannel
        await subsdb.delete_one({"bot_id": self.me.id, "sub_channel": sub_channel})


    async def get_sub_channel(self: "fipper.Client"):
        subsdb = self.mongo_async.subschannel
        r = await subsdb.find_one({"bot_id": self.me.id})
        if r:
            return r['sub_channel']
        else:
            return None
