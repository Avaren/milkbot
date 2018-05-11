import asyncio
import ujson
import os
import uuid


class Config:
    """The "database" object. Internally based on ``json``."""

    def __init__(self, name, **options):
        self.name = name
        self.loop = options.pop('loop', asyncio.get_event_loop())
        self.lock = asyncio.Lock()
        self._db = {}
        if options.pop('load_later', False):
            self.loop.create_task(self.load())
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.name, 'r') as f:
                self._db = ujson.load(f)
        except FileNotFoundError:
            pass

    async def load(self):
        with await self.lock:
            self.load_from_file()

    def _dump(self):
        temp = '%s-%s.tmp' % (uuid.uuid4(), self.name)
        with open(temp, 'w', encoding='utf-8') as tmp:
            ujson.dump(self._db.copy(), tmp, ensure_ascii=False)

        # atomically move the file
        os.replace(temp, self.name)

    async def save(self):
        with await self.lock:
            await self.loop.run_in_executor(None, self._dump)

    def get(self, key, *args):
        """Retrieves a config entry."""
        return self._db.get(key, *args)

    async def put(self, key, value, *args):
        """Edits a config entry."""
        self._db[key] = value
        await self.save()

    async def put_many(self, items):
        """Edits many config entries."""
        self._db.update(items)
        await self.save()

    async def remove(self, key):
        """Removes a config entry."""
        del self._db[key]
        await self.save()

    async def remove_many(self, *keys):
        """Removes a config entry."""
        for key in keys:
            del self._db[key]
        await self.save()

    def __contains__(self, item):
        return item in self._db

    def __getitem__(self, item):
        return self._db[item]

    def __len__(self):
        return len(self._db)

    def all(self):
        return self._db
