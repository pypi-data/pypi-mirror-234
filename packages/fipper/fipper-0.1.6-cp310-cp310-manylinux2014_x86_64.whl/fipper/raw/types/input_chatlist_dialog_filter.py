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


class InputChatlistDialogFilter(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.InputChatlist`.

    Details:
        - Layer: ``158``
        - ID: ``F3E0DA33``

    Parameters:
        filter_id (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["filter_id"]

    ID = 0xf3e0da33
    QUALNAME = "types.InputChatlistDialogFilter"

    def __init__(self, *, filter_id: int) -> None:
        self.filter_id = filter_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputChatlistDialogFilter":
        # No flags
        
        filter_id = Int.read(b)
        
        return InputChatlistDialogFilter(filter_id=filter_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.filter_id))
        
        return b.getvalue()
