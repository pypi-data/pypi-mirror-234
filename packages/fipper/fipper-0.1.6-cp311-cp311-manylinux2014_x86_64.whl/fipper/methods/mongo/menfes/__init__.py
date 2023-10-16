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

from .channels import Channels
from .coin import Coin
from .foto_menfes import FotoMenfes
from .free_coin import FreeCoin
from .hastag import HasTag
from .subs import Subs


class Menfes(
    Channels,
    Coin,
    FotoMenfes,
    FreeCoin,
    HasTag,
    Subs,
):
    pass
