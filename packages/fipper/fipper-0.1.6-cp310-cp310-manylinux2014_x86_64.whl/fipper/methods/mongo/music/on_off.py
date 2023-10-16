


import fipper


class OnOffMusic:
    # On Off
    async def is_on_off(self: 'fipper.Client', on_off: int) -> bool:
        onoffdb = self.mongo_async.on_off_music
        onoff = await onoffdb.find_one({"on_off": on_off})
        if not onoff:
            return False
        return True


    async def add_on(self: 'fipper.Client', on_off: int):
        onoffdb = self.mongo_async.on_off_music
        is_on = await self.is_on_off(on_off)
        if is_on:
            return
        return await onoffdb.insert_one({"on_off": on_off})


    async def add_off(self: 'fipper.Client', on_off: int):
        onoffdb = self.mongo_async.on_off_music
        is_off = await self.is_on_off(on_off)
        if not is_off:
            return
        return await onoffdb.delete_one({"on_off": on_off})