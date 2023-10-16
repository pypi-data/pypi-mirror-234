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


class GroupCallStreamChannel(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.GroupCallStreamChannel`.

    Details:
        - Layer: ``158``
        - ID: ``80EB48AF``

    Parameters:
        channel (``int`` ``32-bit``):
            N/A

        scale (``int`` ``32-bit``):
            N/A

        last_timestamp_ms (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["channel", "scale", "last_timestamp_ms"]

    ID = 0x80eb48af
    QUALNAME = "types.GroupCallStreamChannel"

    def __init__(self, *, channel: int, scale: int, last_timestamp_ms: int) -> None:
        self.channel = channel  # int
        self.scale = scale  # int
        self.last_timestamp_ms = last_timestamp_ms  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GroupCallStreamChannel":
        # No flags
        
        channel = Int.read(b)
        
        scale = Int.read(b)
        
        last_timestamp_ms = Long.read(b)
        
        return GroupCallStreamChannel(channel=channel, scale=scale, last_timestamp_ms=last_timestamp_ms)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.channel))
        
        b.write(Int(self.scale))
        
        b.write(Long(self.last_timestamp_ms))
        
        return b.getvalue()
