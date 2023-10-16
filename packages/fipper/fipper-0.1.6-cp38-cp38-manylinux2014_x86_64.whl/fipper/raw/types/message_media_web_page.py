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


class MessageMediaWebPage(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.MessageMedia`.

    Details:
        - Layer: ``158``
        - ID: ``A32DD600``

    Parameters:
        webpage (:obj:`WebPage <fipper.raw.base.WebPage>`):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: fipper.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetWebPagePreview
            messages.UploadMedia
            messages.UploadImportedMedia
    """

    __slots__: List[str] = ["webpage"]

    ID = 0xa32dd600
    QUALNAME = "types.MessageMediaWebPage"

    def __init__(self, *, webpage: "raw.base.WebPage") -> None:
        self.webpage = webpage  # WebPage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaWebPage":
        # No flags
        
        webpage = TLObject.read(b)
        
        return MessageMediaWebPage(webpage=webpage)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.webpage.write())
        
        return b.getvalue()
