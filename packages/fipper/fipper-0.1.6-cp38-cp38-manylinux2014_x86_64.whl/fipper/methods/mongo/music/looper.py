import fipper


class Looper:
    # LOOP PLAY
    async def get_loop(self: 'fipper.Client', chat_id: int) -> int:
        lop = self.loops.get(chat_id)
        if not lop:
            return 0
        return lop


    async def set_loop(self: 'fipper.Client', chat_id: int, mode: int):
        self.loops[chat_id] = mode