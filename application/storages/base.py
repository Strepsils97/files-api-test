import abc
import os
from typing import IO


class BaseFileStorage(abc.ABC):

    def exists(self, path):
        path = self.get_full_path(path)
        return os.path.exists(path)

    def get_full_path(self, relative_path) -> str:
        return relative_path

    @abc.abstractmethod
    async def get(self, path) -> IO:
        pass

    @abc.abstractmethod
    async def update(self, path, new_content):
        pass

    @abc.abstractmethod
    async def save(self, file, path):
        pass

    @abc.abstractmethod
    async def delete(self, path):
        pass
