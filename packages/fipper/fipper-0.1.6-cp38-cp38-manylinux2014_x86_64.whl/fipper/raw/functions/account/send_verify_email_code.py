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


class SendVerifyEmailCode(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``98E037BB``

    Parameters:
        purpose (:obj:`EmailVerifyPurpose <fipper.raw.base.EmailVerifyPurpose>`):
            N/A

        email (``str``):
            N/A

    Returns:
        :obj:`account.SentEmailCode <fipper.raw.base.account.SentEmailCode>`
    """

    __slots__: List[str] = ["purpose", "email"]

    ID = 0x98e037bb
    QUALNAME = "functions.account.SendVerifyEmailCode"

    def __init__(self, *, purpose: "raw.base.EmailVerifyPurpose", email: str) -> None:
        self.purpose = purpose  # EmailVerifyPurpose
        self.email = email  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendVerifyEmailCode":
        # No flags
        
        purpose = TLObject.read(b)
        
        email = String.read(b)
        
        return SendVerifyEmailCode(purpose=purpose, email=email)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.purpose.write())
        
        b.write(String(self.email))
        
        return b.getvalue()
