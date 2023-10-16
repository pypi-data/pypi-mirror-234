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


class PrivacyValueAllowChatParticipants(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.PrivacyRule`.

    Details:
        - Layer: ``158``
        - ID: ``6B134E8E``

    Parameters:
        chats (List of ``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["chats"]

    ID = 0x6b134e8e
    QUALNAME = "types.PrivacyValueAllowChatParticipants"

    def __init__(self, *, chats: List[int]) -> None:
        self.chats = chats  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PrivacyValueAllowChatParticipants":
        # No flags
        
        chats = TLObject.read(b, Long)
        
        return PrivacyValueAllowChatParticipants(chats=chats)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.chats, Long))
        
        return b.getvalue()
