import hashlib

from asgiref.sync import sync_to_async

CHUNK_SIZE = 32 * 1024  # 32 kb


async def get_file_hash_file(file_obj):
    sha1 = hashlib.sha1()
    file_obj.seek(0)
    while True:
        chunk = await file_obj.read(CHUNK_SIZE)
        if not chunk:
            yield None, sha1.hexdigest()
            return
        await sync_to_async(sha1.update)(chunk)
        yield chunk, sha1.hexdigest()
