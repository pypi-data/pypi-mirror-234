# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from .admins import Admins
from .antipinchannel import AntiPinChannel
from .antiservice import AntiService
from .notes import Notes
from .warn import Warn
from .welcome import Welcome


class Manage(
    Admins,
    AntiPinChannel,
    AntiService,
    Notes,
    Warn,
    Welcome,
):
    pass
