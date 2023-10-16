#  Fipper - Telegram MTProto API Client Library for Python.
#  Copyright (C) 2022-2023 AyiinXd <https://github.com/AyiinXd>
#
#  This file is part of Fipper.
#
#  Fipper is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Fipper is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Fipper.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from fipper.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from fipper.raw.core import TLObject
from fipper import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class GetBotInfo(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``DCD914FD``

    Parameters:
        lang_code (``str``):
            N/A

        bot (:obj:`InputUser <fipper.raw.base.InputUser>`, *optional*):
            N/A

    Returns:
        :obj:`bots.BotInfo <fipper.raw.base.bots.BotInfo>`
    """

    __slots__: List[str] = ["lang_code", "bot"]

    ID = 0xdcd914fd
    QUALNAME = "functions.bots.GetBotInfo"

    def __init__(self, *, lang_code: str, bot: "raw.base.InputUser" = None) -> None:
        self.lang_code = lang_code  # string
        self.bot = bot  # flags.0?InputUser

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBotInfo":
        
        flags = Int.read(b)
        
        bot = TLObject.read(b) if flags & (1 << 0) else None
        
        lang_code = String.read(b)
        
        return GetBotInfo(lang_code=lang_code, bot=bot)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.bot is not None else 0
        b.write(Int(flags))
        
        if self.bot is not None:
            b.write(self.bot.write())
        
        b.write(String(self.lang_code))
        
        return b.getvalue()
