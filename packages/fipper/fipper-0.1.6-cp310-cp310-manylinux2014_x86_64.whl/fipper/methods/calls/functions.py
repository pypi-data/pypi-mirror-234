#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from datetime import datetime, timedelta
from typing import Union

import fipper
from fipper.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from fipper.stream_type import StreamType
from fipper.exception import (
    AlreadyJoinedError,
    ExceptionDetected,
    NoActiveGroupCall,
    TelegramServerError,
)
from fipper.xdcalls import (
    JoinedGroupCallParticipant,
    LeftGroupCallParticipant,
    Update,
)
from fipper.xdcalls.input_stream import AudioPiped, AudioVideoPiped
from fipper.xdcalls.stream import StreamAudioEnded



class CallsFunctions:
    AUTO_END_TIME = 3
    async def pause_stream(self: 'fipper.Client', chat_id: int):
        await self.call.pause_stream(chat_id)

    async def resume_stream(self: 'fipper.Client', chat_id: int):
        await self.call.resume_stream(chat_id)

    async def mute_stream(self: 'fipper.Client', chat_id: int):
        await self.call.mute_stream(chat_id)

    async def unmute_stream(self: 'fipper.Client', chat_id: int):
        await self.call.unmute_stream(chat_id)

    async def stop_stream(self: 'fipper.Client', chat_id: int):
        try:
            self.clear_queue(chat_id)
            await self.call.leave_group_call(chat_id)
            await self.clear_stream(chat_id)
        except:
            pass

    async def clear_stream(self: 'fipper.Client', chat_id: int):
        try:
            await self.remove_active_video_chat(chat_id)
        except:
            pass
        try:
            await self.remove_active_voice_chat(chat_id)
        except:
            pass

    async def participant_stream(
        self: 'fipper.Client',
        update,
    ):
        chat_id = update.chat_id
        if chat_id in self.queue:
            queues = self.get_queue(chat_id)
            if await self.is_autoend():
                try:
                    got = len(await self.call.get_participants(chat_id))
                except:
                    return
                if got == 1:
                    await asyncio.sleep(20)
                    await self.send_message(
                        chat_id=queues[0][0],
                        text="Bot telah meninggalkan obrolan suara karena tidak ada yang mendengarkan bot di obrolan suara dan untuk menghindari kelebihan beban server.",
                    )
                    await self.stop_stream(chat_id)

    async def skip_stream(
        self: 'fipper.Client',
        chat_id: int,
        link: str,
        video: Union[bool, str] = None
    ):
        audio_stream_quality = await self.get_audio_bitrate(chat_id)
        video_stream_quality = await self.get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(
                link, audio_parameters=audio_stream_quality
            )
        )
        await self.call.change_stream(
            chat_id,
            stream,
        )

    async def seek_stream(
        self: 'fipper.Client',
        chat_id,
        file_path,
        to_seek,
        duration,
        mode
    ):
        audio_stream_quality = await self.get_audio_bitrate(chat_id)
        video_stream_quality = await self.get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else AudioPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
        )
        await self.call.change_stream(chat_id, stream)

    async def stream_call(self: 'fipper.Client', chat_id, url):
        try:
            await self.call.join_group_call(
                chat_id,
                AudioVideoPiped(
                    url
                ),
                stream_type=StreamType().pulse_stream,
            )
            await asyncio.sleep(0.5)
            await self.call.leave_group_call(chat_id)
        except:
            pass

    async def join_assistant(self: 'fipper.Client', original_chat_id, chat_id):
        userbot = self.assistant.me
        try:
            try:
                get = await self.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                await self.send_message(
                    chat_id=original_chat_id,
                    text="[ ERROR ] - Bot memerlukan Izin **Admin** untuk mengundang akun asisten ke saluran Anda."
                )
                return
            if get.status == fipper.enums.ChatMemberStatus.BANNED or get.status == fipper.enums.ChatMemberStatus.LEFT:
                await self.send_message(
                    chat_id=original_chat_id,
                    text="[ ERROR ] - Asisten diblokir di grup atau saluran Anda, harap batalkan pemblokiran.\n\n**Nama Pengguna Asisten:** @{}\n**ID Asisten:** {}".format(userbot.username, userbot.id)
                )
                return
        except UserNotParticipant:
            chat = await self.get_chat(chat_id)
            if chat.username:
                try:
                    await self.assistant.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await self.send_message(
                        chat_id=original_chat_id,
                        text="[ ERROR ] - Pengecualian Terjadi Saat Mengundang Akun Asisten ke chat Anda.\n\n**Alasan**: {}".format(e)
                    )
            else:
                try:
                    try:
                        try:
                            invitelink = chat.invite_link
                            if invitelink is None:
                                invitelink = (
                                    await self.export_chat_invite_link(
                                        chat_id
                                    )
                                )
                        except:
                            invitelink = (
                                await self.export_chat_invite_link(
                                    chat_id
                                )
                            )
                    except ChatAdminRequired:
                        await self.send_message(
                            chat_id=original_chat_id,
                            text="[ ERROR ] - Bot memerlukan **Undang Pengguna Melalui Tautan** Izin untuk mengundang akun asisten ke grup obrolan Anda."
                        )
                    except Exception as e:
                        await self.send_message(
                            chat_id=original_chat_id,
                            text=f'[ ERROR ] - {e}'
                        )
                    m = await self.send_message(
                        original_chat_id,
                        "[ INFO ] - Akun Asisten akan bergabung dalam 5 Detik.. Harap Tunggu!"
                    )
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await asyncio.sleep(3)
                    await self.assistant.join_chat(invitelink)
                    await asyncio.sleep(4)
                    await m.edit("[ SUCCESS ] - Akun Asisten[{}] Berhasil Bergabung.\n\nMulai Musik Sekarang".format(userbot.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await self.send_message(original_chat_id, "[ ERROR ] - Pengecualian Terjadi Saat Mengundang Akun Asisten ke chat Anda.\n\n**Alasan**: {}".format(e))

    async def join_call(
        self: 'fipper.Client',
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
    ):
        audio_stream_quality = await self.get_audio_bitrate(chat_id)
        video_stream_quality = await self.get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(
                link, audio_parameters=audio_stream_quality
            )
        )
        try:
            await self.call.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
            except Exception as e:
                await self.send_message(
                    chat_id=original_chat_id,
                    text=f"[ ERROR ] - {e}"
                )
            try:
                await self.call.join_group_call(
                    chat_id,
                    stream,
                    stream_type=StreamType().pulse_stream,
                )
            except Exception as e:
                await self.send_message(
                    chat_id=original_chat_id,
                    text="**[ ERROR ] - No Active Voice Chat Found**\n\nPlease make sure group's voice chat is enabled. If already enabled, please end it and start fresh voice chat again and if the problem continues, try /restart"
                )
        except AlreadyJoinedError:
            await self.send_message(
                chat_id=original_chat_id,
                text="**[ ERROR ] - Assistant Already in Voice Chat**\n\nSystems have detected that assistant is already there in the voice chat, this issue generally comes when you play 2 queries together.\n\nIf assistant is not present in voice chat, please end voice chat and start fresh voice chat again and if the  problem continues, try /restart"
            )
        except TelegramServerError:
            await self.send_message(
                chat_id=original_chat_id,
                text="**[ ERROR ] - Telegram Server Error**\n\nTelegram is having some internal server problems, Please try playing again.\n\n If this problem keeps coming everytime, please end your voice chat and start fresh voice chat again."
            )
        if video:
            vcg = await self.get_active_video_chats()
            if chat_id not in vcg:
                await self.add_active_video_chat(chat_id)
        else:
            vc = await self.get_active_voice_chats()
            if chat_id not in vc:
                await self.add_active_voice_chat(chat_id)

    async def change_stream(
        self: 'fipper.Client',
        chat_id
    ):
        audio_stream_quality = await self.get_audio_bitrate(chat_id)
        video_stream_quality = await self.get_video_bitrate(chat_id)
        try:
            if chat_id in self.queue:
                chat_queue = self.get_queue(chat_id)
                if len(chat_queue) == 1:
                    await self.call.leave_group_call(chat_id)
                    self.clear_queue(chat_id)
                    await self.clear_stream(chat_id)
                    return 1
                else:
                    orifinal_chat_id = chat_queue[1][0]
                    songname = chat_queue[1][1]
                    file_path = chat_queue[1][2]
                    link = chat_queue[1][3]
                    video = chat_queue[1][4]
                    videoid = chat_queue[1][5]
                    user_id = chat_queue[1][6]
                    if videoid is not None:
                        thumbs = await self.gen_thumb(videoid=videoid, user_id=user_id, queue=False)
                        duration_min = await self.duration_youtube(link=videoid, videoid=True)
                    else:
                        thumbs = "https://telegra.ph//file/91e6c6b28b36481251c8b.jpg"
                        duration_min = "Unknown"
                    try:
                        mention = (await self.get_users(user_id)).mention
                    except:
                        mention = user_id
                    song_mention = f"<a href={link}>{songname}</a>"
                    stream = (
                        AudioVideoPiped(
                            file_path,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                        if video == True
                        else AudioPiped(
                            file_path, audio_parameters=audio_stream_quality
                        )
                    )
                    await self.call.change_stream(
                        chat_id,
                        stream,
                    )
                    await self.send_photo(
                        orifinal_chat_id,
                        photo=thumbs,
                        caption=f"""
<b>▶ Memainkan lagu berikutnya</b>

<b>🏷️ Judul:</b> {song_mention}
<b>⏱️ Durasi:<b> {duration_min} Mins
<b>🎧 Atas permintaan:</b> {mention}
"""
                    )
                    self.pop_an_item(chat_id)
                    type = "Video" if video == True else "Audio"
                    return [songname, link, type]
            else:
                return 0
        except Exception as e:
            print(f'SKIP_SONG ERROR: {e}')

    async def decorators(self: 'fipper.Client'):
        @self.call.on_kicked()
        @self.call.on_closed_voice_chat()
        @self.call.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.call.on_stream_end()
        async def stream_end_handler1(_, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.change_stream(update.chat_id)

        @self.call.on_participants_change()
        async def participants_change_handler(_, update: Update):
            await self.participant_stream(update)
            """
            if not isinstance(
                update, JoinedGroupCallParticipant
            ) and not isinstance(update, LeftGroupCallParticipant):
                return
            chat_id = update.chat_id
            """
