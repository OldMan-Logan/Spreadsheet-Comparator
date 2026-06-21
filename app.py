from fastapi import FastAPI
from fastapi import UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from compare import compare_files

import shutil
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
# async def home(request: Request):

#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request}
#     )
# @app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/compare")
async def compare(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):

    os.makedirs("uploads", exist_ok=True)

    path1 = f"uploads/{file1.filename}"
    path2 = f"uploads/{file2.filename}"

    with open(path1, "wb") as f:
        shutil.copyfileobj(file1.file, f)

    with open(path2, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    result = compare_files(path1, path2)

    return templates.TemplateResponse(
    request=request,
    name="results.html",
    context={
        "result": result
    }
    )