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

ReportReason = Union[raw.types.InputReportReasonChildAbuse, raw.types.InputReportReasonCopyright, raw.types.InputReportReasonFake, raw.types.InputReportReasonGeoIrrelevant, raw.types.InputReportReasonIllegalDrugs, raw.types.InputReportReasonOther, raw.types.InputReportReasonPersonalDetails, raw.types.InputReportReasonPornography, raw.types.InputReportReasonSpam, raw.types.InputReportReasonViolence]


# noinspection PyRedeclaration
class ReportReason:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 10 constructors available.

        .. currentmodule:: fipper.raw.types

        .. autosummary::
            :nosignatures:

            InputReportReasonChildAbuse
            InputReportReasonCopyright
            InputReportReasonFake
            InputReportReasonGeoIrrelevant
            InputReportReasonIllegalDrugs
            InputReportReasonOther
            InputReportReasonPersonalDetails
            InputReportReasonPornography
            InputReportReasonSpam
            InputReportReasonViolence
    """

    QUALNAME = "fipper.raw.base.ReportReason"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/report-reason")
