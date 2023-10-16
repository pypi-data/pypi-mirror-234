#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

import fipper


class Tools:
    formats = [
        "webm",
        "mkv",
        "flv",
        "vob",
        "ogv",
        "ogg",
        "rrc",
        "gifv",
        "mng",
        "mov",
        "avi",
        "qt",
        "wmv",
        "yuv",
        "rm",
        "asf",
        "amv",
        "mp4",
        "m4p",
        "m4v",
        "mpg",
        "mp2",
        "mpeg",
        "mpe",
        "mpv",
        "m4v",
        "svi",
        "3gp",
        "3g2",
        "mxf",
        "roq",
        "nsv",
        "flv",
        "f4v",
        "f4p",
        "f4a",
        "f4b",
    ]

    def get_readable_time(self: 'fipper.Client', seconds: int) -> str:
        count = 0
        ping_time = ""
        time_list = []
        time_suffix_list = ["s", "m", "h", "days"]
        while count < 4:
            count += 1
            if count < 3:
                remainder, result = divmod(seconds, 60)
            else:
                remainder, result = divmod(seconds, 24)
            if seconds == 0 and remainder == 0:
                break
            time_list.append(int(result))
            seconds = int(remainder)
        for i in range(len(time_list)):
            time_list[i] = str(time_list[i]) + time_suffix_list[i]
        if len(time_list) == 4:
            ping_time += time_list.pop() + ", "
        time_list.reverse()
        ping_time += ":".join(time_list)
        return ping_time


    def convert_bytes(self: 'fipper.Client', size: float) -> str:
        """humanize size"""
        if not size:
            return ""
        power = 1024
        t_n = 0
        power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
        while size > power:
            size /= power
            t_n += 1
        return "{:.2f} {}B".format(size, power_dict[t_n])


    async def int_to_alpha(self: 'fipper.Client', user_id: int) -> str:
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        text = ""
        user_id = str(user_id)
        for i in user_id:
            text += alphabet[int(i)]
        return text


    async def alpha_to_int(self: 'fipper.Client', user_id_alphabet: str) -> int:
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        user_id = ""
        for i in user_id_alphabet:
            index = alphabet.index(i)
            user_id += str(index)
        user_id = int(user_id)
        return user_id


    def time_to_seconds(self: 'fipper.Client', time):
        stringt = str(time)
        return sum(
            int(x) * 60**i
            for i, x in enumerate(reversed(stringt.split(":")))
        )


    def seconds_to_min(self: 'fipper.Client', seconds):
        if seconds is not None:
            seconds = int(seconds)
            d, h, m, s = (
                seconds // (3600 * 24),
                seconds // 3600 % 24,
                seconds % 3600 // 60,
                seconds % 3600 % 60,
            )
            if d > 0:
                return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
            elif h > 0:
                return "{:02d}:{:02d}:{:02d}".format(h, m, s)
            elif m > 0:
                return "{:02d}:{:02d}".format(m, s)
            elif s > 0:
                return "00:{:02d}".format(s)
        return "-"

    async def shell_cmd(self: 'fipper.Client', cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, errorz = await proc.communicate()
        if errorz:
            if (
                "unavailable videos are hidden"
                in (errorz.decode("utf-8")).lower()
            ):
                return out.decode("utf-8")
            else:
                return errorz.decode("utf-8")
        return out.decode("utf-8")
