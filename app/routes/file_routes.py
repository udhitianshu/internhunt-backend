# app/routes/file_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["Files"])

@router.get("/download/{filename}")
def download_file(filename: str):
    safe = os.path.basename(filename)
    path = os.path.join("temp_uploads", safe)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/pdf", filename=safe)
