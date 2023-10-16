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


class PlayType:
    async def get_play_type(self: "fipper.Client", chat_id) -> bool:
        """Get Play Typer Mode admin or Everyone by Your Bots.

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

                await app.get_play_type(chat_id)
        """
        privatemodedb = self.mongo_async.play_type
        chat = await privatemodedb.find_one({"chat_id": chat_id})
        if not chat:
            return False
        return chat['mode']


    async def set_play_type(self: "fipper.Client", chat_id, mode: bool = None):
        """Set Play Typer Mode admin or Everyone by Your Bots.

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

                await app.set_play_type(chat_id, mode)
        """
        channelmodedb = self.mongo_async.play_type
        is_antiservice = await channelmodedb.find_one({"chat_id": chat_id})
        if mode:
            if is_antiservice:
                await channelmodedb.update_one(
                    {"chat_id": chat_id},
                    {
                        "$set": {
                            "mode": mode
                        }
                    }
                )
            else:
                return await channelmodedb.insert_one({"chat_id": chat_id, "mode": mode})
        else:
            if is_antiservice:
                await channelmodedb.update_one(
                    {"chat_id": chat_id},
                    {
                        "$set": {
                            "mode": False
                        }
                    }
                )
            else:
                return await channelmodedb.insert_one({"chat_id": chat_id, "mode": False})
