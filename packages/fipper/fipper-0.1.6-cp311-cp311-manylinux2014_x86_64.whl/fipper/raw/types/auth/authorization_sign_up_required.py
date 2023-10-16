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


class AuthorizationSignUpRequired(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~fipper.raw.base.auth.Authorization`.

    Details:
        - Layer: ``158``
        - ID: ``44747E9A``

    Parameters:
        terms_of_service (:obj:`help.TermsOfService <fipper.raw.base.help.TermsOfService>`, *optional*):
            N/A

    Functions:
        This object can be returned by 7 functions.

        .. currentmodule:: fipper.raw.functions

        .. autosummary::
            :nosignatures:

            auth.SignUp
            auth.SignIn
            auth.ImportAuthorization
            auth.ImportBotAuthorization
            auth.CheckPassword
            auth.RecoverPassword
            auth.ImportWebTokenAuthorization
    """

    __slots__: List[str] = ["terms_of_service"]

    ID = 0x44747e9a
    QUALNAME = "types.auth.AuthorizationSignUpRequired"

    def __init__(self, *, terms_of_service: "raw.base.help.TermsOfService" = None) -> None:
        self.terms_of_service = terms_of_service  # flags.0?help.TermsOfService

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AuthorizationSignUpRequired":
        
        flags = Int.read(b)
        
        terms_of_service = TLObject.read(b) if flags & (1 << 0) else None
        
        return AuthorizationSignUpRequired(terms_of_service=terms_of_service)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.terms_of_service is not None else 0
        b.write(Int(flags))
        
        if self.terms_of_service is not None:
            b.write(self.terms_of_service.write())
        
        return b.getvalue()
