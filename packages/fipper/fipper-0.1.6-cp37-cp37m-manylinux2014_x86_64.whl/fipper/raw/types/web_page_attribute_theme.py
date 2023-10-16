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


class WebPageAttributeTheme(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.WebPageAttribute`.

    Details:
        - Layer: ``158``
        - ID: ``54B56617``

    Parameters:
        documents (List of :obj:`Document <fipper.raw.base.Document>`, *optional*):
            N/A

        settings (:obj:`ThemeSettings <fipper.raw.base.ThemeSettings>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["documents", "settings"]

    ID = 0x54b56617
    QUALNAME = "types.WebPageAttributeTheme"

    def __init__(self, *, documents: Optional[List["raw.base.Document"]] = None, settings: "raw.base.ThemeSettings" = None) -> None:
        self.documents = documents  # flags.0?Vector<Document>
        self.settings = settings  # flags.1?ThemeSettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPageAttributeTheme":
        
        flags = Int.read(b)
        
        documents = TLObject.read(b) if flags & (1 << 0) else []
        
        settings = TLObject.read(b) if flags & (1 << 1) else None
        
        return WebPageAttributeTheme(documents=documents, settings=settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.documents else 0
        flags |= (1 << 1) if self.settings is not None else 0
        b.write(Int(flags))
        
        if self.documents is not None:
            b.write(Vector(self.documents))
        
        if self.settings is not None:
            b.write(self.settings.write())
        
        return b.getvalue()
