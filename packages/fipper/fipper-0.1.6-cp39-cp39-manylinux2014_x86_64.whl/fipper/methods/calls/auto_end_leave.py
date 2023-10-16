import asyncio
from datetime import datetime

import fipper


class AutoEndLeave:
    async def auto_leave(self: 'fipper.Client'):
        left = 0
        ChatType = fipper.enums.ChatType
        log = await self.get_logs()
        mode = await self.get_leave_assistant()
        leave_time = await self.get_leave_assistant_time()
        if mode:
            while not await asyncio.sleep(
                leave_time
            ):
                try:
                    async for i in self.assistant.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if (
                                chat_id != int(log)
                                and chat_id != -1001797285258
                            ):
                                if left == 20:
                                    continue
                                if chat_id not in self.queue:
                                    try:
                                        await self.assistant.leave_chat(
                                            chat_id
                                        )
                                        left += 1
                                    except:
                                        continue
                except:
                    pass
        self.loop.create_task(self.auto_leave())
