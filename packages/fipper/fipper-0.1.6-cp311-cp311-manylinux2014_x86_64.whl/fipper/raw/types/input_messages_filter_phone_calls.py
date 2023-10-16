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


class InputMessagesFilterPhoneCalls(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.MessagesFilter`.

    Details:
        - Layer: ``158``
        - ID: ``80C99768``

    Parameters:
        missed (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["missed"]

    ID = 0x80c99768
    QUALNAME = "types.InputMessagesFilterPhoneCalls"

    def __init__(self, *, missed: Optional[bool] = None) -> None:
        self.missed = missed  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMessagesFilterPhoneCalls":
        
        flags = Int.read(b)
        
        missed = True if flags & (1 << 0) else False
        return InputMessagesFilterPhoneCalls(missed=missed)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.missed else 0
        b.write(Int(flags))
        
        return b.getvalue()
