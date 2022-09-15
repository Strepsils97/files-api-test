import os
from typing import IO

import aiofiles
from asgiref.sync import sync_to_async

from application import settings
from application.storages.base import BaseFileStorage


class LocalFileStorage(BaseFileStorage):

    CHUNK_SIZE = 1024 * 32  # 32 kb
    root_directory = os.path.join(settings.BASE_DIR, "media")

    def get_full_path(self, relative_path):
        return os.path.join(self.root_directory, relative_path)

    async def get_info(self, path):
        path = self.get_full_path(path)
        name = await sync_to_async(os.path.basename)(path)
        size = await sync_to_async(os.path.getsize)(path)
        last_modified = await sync_to_async(os.path.getmtime)(path)
        created_at = await sync_to_async(os.path.getctime)(path)
        return dict(
            name=name,
            size=size,
            last_modified=last_modified,
            created_at=created_at,
        )

    async def get_chunks(self, path):
        path = self.get_full_path(path)
        async with aiofiles.open(path, "rb") as file:
            while True:
                chunk = await file.read(self.CHUNK_SIZE)
                if not chunk:
                    return
                yield chunk

    async def get(self, path) -> IO:
        path = self.get_full_path(path)
        async with aiofiles.open(path, "rb") as file:
            return await file.read()

    async def update(self, path, new_content):
        path = self.get_full_path(path)
        async with aiofiles.open(path, "a+b") as file:
            await file.write(new_content)

    async def save(self, file, path):
        path = self.get_full_path(path)
        async with aiofiles.open(path, "wb") as file_obj:
            await file_obj.write(file)

    async def delete(self, path):
        path = self.get_full_path(path)
        await sync_to_async(os.remove)(path)
