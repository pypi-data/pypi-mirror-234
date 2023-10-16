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

import fipper
from fipper.viper_client import ViperCalls


class Assistant:
    def get_assistant(self: "fipper.Client"):
        if self.assistant is None:
            name, api_id, api_hash, session = self.get_ubot()
            assistants = fipper.Client(
                name=name,
                api_id=api_id,
                api_hash=api_hash,
                session_string=session,
            )
            self.assistant = assistants
            return self.assistant
        else:
            return self.assistant

    def get_viper(self: "fipper.Client"):
        if self.call is None:
            self.assistant = self.get_assistant()
            calls = ViperCalls(
                assistant=self.assistant,
                cache_duration=100,
            )
            self.call = calls
            return self.call
        else:
            return self.call
