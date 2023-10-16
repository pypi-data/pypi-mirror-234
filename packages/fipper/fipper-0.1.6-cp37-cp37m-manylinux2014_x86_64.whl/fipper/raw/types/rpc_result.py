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


class RpcResult(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.RpcResult`.

    Details:
        - Layer: ``158``
        - ID: ``F35C6D01``

    Parameters:
        req_msg_id (``int`` ``64-bit``):
            N/A

        result (:obj:`Object <fipper.raw.base.Object>`):
            N/A

    """

    __slots__: List[str] = ["req_msg_id", "result"]

    ID = 0xf35c6d01
    QUALNAME = "types.RpcResult"

    def __init__(self, *, req_msg_id: int, result: TLObject) -> None:
        self.req_msg_id = req_msg_id  # long
        self.result = result  # Object

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RpcResult":
        # No flags
        
        req_msg_id = Long.read(b)
        
        result = TLObject.read(b)
        
        return RpcResult(req_msg_id=req_msg_id, result=result)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        b.write(self.result.write())
        
        return b.getvalue()
