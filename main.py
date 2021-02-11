import os
import sys

if not os.getenv("DEBUG"):
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), "deps"))

from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from mustachify import mustachify

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def normalize(ext):
    return {"JPG": "jpeg"}.get(ext.upper(), ext)


@app.get("/", response_class=HTMLResponse)
async def index():
    return open("./index.html").read()


@app.post("/files/")
def _mustachify(file: UploadFile = File(...)):
    b = BytesIO()
    img = mustachify(file.file)
    ext = normalize(file.filename.split(".")[-1])
    img.save(b, format=ext)
    b.seek(0)
    return StreamingResponse(b)
