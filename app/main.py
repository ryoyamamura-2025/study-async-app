# app/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Hello</title></head>
      <body style="font-family:system-ui; margin:40px;">
        <h1>FastAPI + uv (editable)</h1>
        <p>これはルートaaaaa <code>/</code> に HTML を返すデモです。</p>
      </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)