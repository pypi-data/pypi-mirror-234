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

from typing import Union

import fipper


class ChannelMode:
    async def is_channel_mode(self: "fipper.Client", chat_id) -> bool:
        """Get Play Channel Mode by Your Bots.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            List of :obj:`~fipper.types.Message`: On success, a list of copied messages is returned.

        Example:
            .. code-block:: python

                # Copy a media group
                await app.get_channel_mode(chat_id)
        """
        privatemodedb = self.mongo_async.channel_mode
        chat = await privatemodedb.find_one({"chat_id": chat_id})
        if not chat:
            return False
        return True


    async def get_channel_mode(self: "fipper.Client", chat_id):
        """Get Play Channel Mode by Your Bots.
            
            Example:
                await app.get_channel_mode(chat_id)
        """
        privatemodedb = self.mongo_async.channel_mode
        chat = await privatemodedb.find_one({"chat_id": chat_id})
        if not chat:
            return None
        return chat['channel_id']


    async def set_channel_mode(self: "fipper.Client", chat_id: int, channel_id: int, channel_mode: Union[bool, str] = None):
        """Set Play Channel Mode by Your Bots.
            
            Example:
                await app.set_channel_mode(chat_id, mode)
        """
        channelmodedb = self.mongo_async.channel_mode
        is_antiservice = await channelmodedb.find_one({"chat_id": chat_id})
        if channel_mode:
            if is_antiservice:
                await channelmodedb.update_one(
                    {"chat_id": chat_id},
                    {
                        "$set": {
                            "channel_id": channel_id
                        }
                    }
                )
            else:
                return await channelmodedb.insert_one({"chat_id": chat_id, "channel_id": channel_id})
        else:
            await channelmodedb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "channel_id": None
                    }
                }
            )
            return 
