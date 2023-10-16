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

from .active_voice_video import ActiveVoiceVideo
from .assistant import Assistant
from .auto_end import AutoEnd
from .auto_leave_assistant import AutoLeaveAssistant
from .bit_rate import BitRate
from .channel_mode import ChannelMode
from .chat_support import ChatSupport
from .looper import Looper
from .on_off import OnOffMusic
from .play_mode import PlayMode
from .play_type import PlayType
from .private_mode import PrivateMode
from .queues import Queues
from .skip_pause import SkipPause


class Music(
    ActiveVoiceVideo,
    Assistant,
    AutoEnd,
    AutoLeaveAssistant,
    BitRate,
    ChannelMode,
    ChatSupport,
    Looper,
    OnOffMusic,
    PlayMode,
    PlayType,
    PrivateMode,
    Queues,
    SkipPause,
):
    pass
