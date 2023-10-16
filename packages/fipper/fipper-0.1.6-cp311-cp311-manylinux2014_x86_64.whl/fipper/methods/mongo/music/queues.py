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
from fipper.xdcalls.input_stream import AudioPiped, AudioVideoPiped


class Queues:
    def add_to_queue(
        self: 'fipper.Client',
        chat_id: int,
        original_chat_id: int,
        songname: str,
        file_path,
        link: str,
        video: bool,
        videoid: str,
        user_id: int,
    ):
        if chat_id in self.queue:
            chat_queue = self.queue[chat_id]
            chat_queue.append([original_chat_id, songname, file_path, link, video, videoid, user_id])
            return int(len(chat_queue) - 1)
        self.queue[chat_id] = [[original_chat_id, songname, file_path, link, video, videoid, user_id]]

    def get_queue(self: 'fipper.Client', chat_id):
        if chat_id in self.queue:
            return self.queue[chat_id]
        return 0

    def pop_an_item(self: 'fipper.Client', chat_id):
        if chat_id in self.queue:
            chat_queue = self.queue[chat_id]
            chat_queue.pop(0)
            return 1
        return 0

    def clear_queue(self: 'fipper.Client', chat_id: int):
        if chat_id in self.queue:
            self.queue.pop(chat_id)
            return 1
        return 0

    async def skip_item(self: 'fipper.Client', chat_id, h):
        if chat_id in self.queue:
            chat_queue = self.get_queue(chat_id)
            try:
                x = int(h)
                songname = chat_queue[x][1]
                chat_queue.pop(x)
                return songname
            except Exception as e:
                print(e)
                return 0
        else:
            return 0
