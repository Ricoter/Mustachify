import random
import gc
import os
from os.path import join, dirname, abspath
import sys

if not os.getenv("DEBUG"):
    sys.path.insert(0, join(abspath(dirname(dirname(__file__))), "deps"))

from io import BytesIO

from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from mustachify import mustachify

app = FastAPI()

app.mount("/static", StaticFiles(directory=join(abspath(dirname(__file__)), "static")), name="static")


def normalize(ext):
    return {"JPG": "jpeg"}.get(ext.upper(), ext)


@app.get("/", response_class=HTMLResponse)
async def index():
    return open("./index.html").read()


@app.post("/files/")
def _mustachify(tasks: BackgroundTasks,file: UploadFile = File(...)):
    b = BytesIO()
    img = mustachify(file.file)
    ext = normalize(file.filename.split(".")[-1])
    img.save(b, format=ext)
    b.seek(0)

    if random.random() < .7:
        tasks.add_task(gc.collect)

    return StreamingResponse(b)
