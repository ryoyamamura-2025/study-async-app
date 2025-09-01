# app/main.py
import os
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(BASE_DIR, 'templetes/index.html'))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)