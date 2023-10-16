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


class TmpPassword(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.account.TmpPassword`.

    Details:
        - Layer: ``158``
        - ID: ``DB64FD34``

    Parameters:
        tmp_password (``bytes``):
            N/A

        valid_until (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: fipper.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetTmpPassword
    """

    __slots__: List[str] = ["tmp_password", "valid_until"]

    ID = 0xdb64fd34
    QUALNAME = "types.account.TmpPassword"

    def __init__(self, *, tmp_password: bytes, valid_until: int) -> None:
        self.tmp_password = tmp_password  # bytes
        self.valid_until = valid_until  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TmpPassword":
        # No flags
        
        tmp_password = Bytes.read(b)
        
        valid_until = Int.read(b)
        
        return TmpPassword(tmp_password=tmp_password, valid_until=valid_until)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.tmp_password))
        
        b.write(Int(self.valid_until))
        
        return b.getvalue()
