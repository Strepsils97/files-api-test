from fastapi import FastAPI

from application.api import routers


app = FastAPI(root_path="api/v1")

app.include_router(routers.files_router, prefix="/files")
