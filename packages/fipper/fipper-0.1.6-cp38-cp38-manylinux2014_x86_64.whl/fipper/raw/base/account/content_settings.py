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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from fipper import raw
from fipper.raw.core import TLObject

ContentSettings = Union[raw.types.account.ContentSettings]


# noinspection PyRedeclaration
class ContentSettings:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: fipper.raw.types

        .. autosummary::
            :nosignatures:

            account.ContentSettings

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: fipper.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetContentSettings
    """

    QUALNAME = "fipper.raw.base.account.ContentSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/content-settings")
