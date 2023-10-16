


import fipper
from fipper.xdcalls.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityAudio,
    LowQualityVideo,
    MediumQualityAudio,
    MediumQualityVideo,
)




class BitRate:
    async def get_bit_video(self: 'fipper.Client', chat_id: int):
        bitvideodb = self.mongo_async.bitrate
        video = await bitvideodb.find_one({"chat_id": chat_id})
        if not video:
            return "High"
        try:
            return video['video_bitrate']
        except KeyError:
            return "High"


    async def get_bit_audio(self: 'fipper.Client', chat_id: int):
        bitvideodb = self.mongo_async.bitrate
        audio = await bitvideodb.find_one({"chat_id": chat_id})
        if not audio:
            return "High"
        try:
            return audio['audio_bitrate']
        except KeyError:
            return "High"


    async def save_audio_bitrate(self: 'fipper.Client', chat_id: int, bitrate: str):
        bitdb = self.mongo_async.bitrate
        bit_audio = await self.get_bit_audio(chat_id)
        if bit_audio:
            await bitdb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "audio_bitrate": bitrate.capitalize()
                    }
                }
            )
        else:
            await bitdb.insert_one({"chat_id": chat_id, "audio_bitrate": bitrate.capitalize()})


    async def save_video_bitrate(self: 'fipper.Client', chat_id: int, bitrate: str):
        bitdb = self.mongo_async.bitrate
        bit_audio = await self.get_bit_video(chat_id)
        if bit_audio:
            await bitdb.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "video_bitrate": bitrate.capitalize()
                    }
                }
            )
        else:
            await bitdb.insert_one({"chat_id": chat_id, "video_bitrate": bitrate.capitalize()})


    async def get_audio_bitrate(self: 'fipper.Client', chat_id: int) -> str:
        mode = await self.get_bit_audio(chat_id)
        if not mode:
            return MediumQualityAudio()
        if str(mode) == "High":
            return HighQualityAudio()
        elif str(mode) == "Medium":
            return MediumQualityAudio()
        elif str(mode) == "Low":
            return LowQualityAudio()


    async def get_video_bitrate(self: 'fipper.Client', chat_id: int) -> str:
        mode = await self.get_bit_video(chat_id)
        private_mode = await self.is_private_mode()
        if not mode:
            if private_mode == str(True):
                return HighQualityVideo()
            else:
                return MediumQualityVideo()
        if str(mode) == "High":
            return HighQualityVideo()
        elif str(mode) == "Medium":
            return MediumQualityVideo()
        elif str(mode) == "Low":
            return LowQualityVideo()
