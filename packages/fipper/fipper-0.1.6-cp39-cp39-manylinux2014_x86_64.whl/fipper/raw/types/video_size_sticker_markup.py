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


class VideoSizeStickerMarkup(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.VideoSize`.

    Details:
        - Layer: ``158``
        - ID: ``DA082FE``

    Parameters:
        stickerset (:obj:`InputStickerSet <fipper.raw.base.InputStickerSet>`):
            N/A

        sticker_id (``int`` ``64-bit``):
            N/A

        background_colors (List of ``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["stickerset", "sticker_id", "background_colors"]

    ID = 0xda082fe
    QUALNAME = "types.VideoSizeStickerMarkup"

    def __init__(self, *, stickerset: "raw.base.InputStickerSet", sticker_id: int, background_colors: List[int]) -> None:
        self.stickerset = stickerset  # InputStickerSet
        self.sticker_id = sticker_id  # long
        self.background_colors = background_colors  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "VideoSizeStickerMarkup":
        # No flags
        
        stickerset = TLObject.read(b)
        
        sticker_id = Long.read(b)
        
        background_colors = TLObject.read(b, Int)
        
        return VideoSizeStickerMarkup(stickerset=stickerset, sticker_id=sticker_id, background_colors=background_colors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stickerset.write())
        
        b.write(Long(self.sticker_id))
        
        b.write(Vector(self.background_colors, Int))
        
        return b.getvalue()
