from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    size: str
    last_modified: str
    created_at: str
