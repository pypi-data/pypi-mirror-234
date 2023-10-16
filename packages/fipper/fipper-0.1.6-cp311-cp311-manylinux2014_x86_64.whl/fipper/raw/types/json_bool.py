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


class JsonBool(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.JSONValue`.

    Details:
        - Layer: ``158``
        - ID: ``C7345E6A``

    Parameters:
        value (``bool``):
            N/A

    """

    __slots__: List[str] = ["value"]

    ID = 0xc7345e6a
    QUALNAME = "types.JsonBool"

    def __init__(self, *, value: bool) -> None:
        self.value = value  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JsonBool":
        # No flags
        
        value = Bool.read(b)
        
        return JsonBool(value=value)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bool(self.value))
        
        return b.getvalue()
