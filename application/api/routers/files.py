from fastapi import APIRouter, Response, UploadFile
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from application.entities.files import FileInfo
from application.storages.storages import LocalFileStorage


router = APIRouter()
storage = LocalFileStorage()


@router.get("/{id}", response_class=StreamingResponse, tags=["files"])
async def get_file(id: str):
    if not storage.exists(id):
        return Response(status_code=404)
    return StreamingResponse(
        storage.get_chunks(id),
        status_code=200,
        media_type="application/octet-stream"
    )


@router.head("/{id}", tags=["files"])
async def file_info(id: str, response: Response):
    if not storage.exists(id):
        return Response(status_code=404)
    data = await storage.get_info(id)
    info = FileInfo(**data)
    response.headers["File-Name"] = info.name
    response.headers["File-Size"] = info.size
    response.headers["File-Created"] = info.created_at
    response.headers["File-Updated"] = info.last_modified
    return {}


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
