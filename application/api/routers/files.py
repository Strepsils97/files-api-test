from fastapi import APIRouter, Response, UploadFile
from starlette.responses import StreamingResponse

from application.storages.storages import LocalFileStorage


router = APIRouter()
storage = LocalFileStorage()


@router.get(
    "/{id}",
    responses={"200": {}},
    response_class=StreamingResponse,
    tags=["files"],
)
async def get_file(id: str):
    if not storage.exists(id):
        return Response(status_code=404)
    return StreamingResponse(
        storage.get_chunks(id),
        status_code=200,
        media_type="application/octet-stream"
    )


@router.head(
    "/{id}",
    responses={"404": {}, "200": {}},
    tags=["files"],
)
async def file_info(id: str):
    if not storage.exists(id):
        return Response(status_code=404)
    name, size, last_modified, created_at = await storage.get_info(id)
    return dict(
        name=name,
        size=size,
        last_modified=last_modified,
        created_at=created_at,
    )


@router.post(
    "/",
    responses={"201": {}},
    tags=["files"],
)
async def save_file(file: UploadFile):
    await storage.save(b"", file.filename)
    while True:
        chunk = await file.read(storage.CHUNK_SIZE)
        if not chunk:
            return Response(status_code=201)
        await storage.update(file.filename, chunk)
