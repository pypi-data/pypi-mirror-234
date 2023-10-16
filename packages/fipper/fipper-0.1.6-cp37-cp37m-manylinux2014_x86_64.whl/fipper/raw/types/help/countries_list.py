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


class CountriesList(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.help.CountriesList`.

    Details:
        - Layer: ``158``
        - ID: ``87D0759E``

    Parameters:
        countries (List of :obj:`help.Country <fipper.raw.base.help.Country>`):
            N/A

        hash (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: fipper.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetCountriesList
    """

    __slots__: List[str] = ["countries", "hash"]

    ID = 0x87d0759e
    QUALNAME = "types.help.CountriesList"

    def __init__(self, *, countries: List["raw.base.help.Country"], hash: int) -> None:
        self.countries = countries  # Vector<help.Country>
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CountriesList":
        # No flags
        
        countries = TLObject.read(b)
        
        hash = Int.read(b)
        
        return CountriesList(countries=countries, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.countries))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
