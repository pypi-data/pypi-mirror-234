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


class ExportedChatlistInvite(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.ExportedChatlistInvite`.

    Details:
        - Layer: ``158``
        - ID: ``C5181AC``

    Parameters:
        title (``str``):
            N/A

        url (``str``):
            N/A

        peers (List of :obj:`Peer <fipper.raw.base.Peer>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: fipper.raw.functions

        .. autosummary::
            :nosignatures:

            chatlists.EditExportedInvite
    """

    __slots__: List[str] = ["title", "url", "peers"]

    ID = 0xc5181ac
    QUALNAME = "types.ExportedChatlistInvite"

    def __init__(self, *, title: str, url: str, peers: List["raw.base.Peer"]) -> None:
        self.title = title  # string
        self.url = url  # string
        self.peers = peers  # Vector<Peer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedChatlistInvite":
        
        flags = Int.read(b)
        
        title = String.read(b)
        
        url = String.read(b)
        
        peers = TLObject.read(b)
        
        return ExportedChatlistInvite(title=title, url=url, peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        
        b.write(Int(flags))
        
        b.write(String(self.title))
        
        b.write(String(self.url))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
