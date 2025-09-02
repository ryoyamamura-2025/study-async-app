# main.py
import os
import asyncio
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Gemini Async Chat Sample")

# 静的ファイル提供 & ルートで index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse('templates/index.html')

# ====== 設定・共通ユーティリティ ======

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
MOCK_MODE = os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes")

# モデル名は要件どおり（変更しやすいように定数化）
MODEL_FLASH_LITE = "gemini-2.5-flash-lite"
MODEL_FLASH = "gemini-2.5-flash"

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

class GreetRequest(BaseModel):
    # JS 側が渡す“型”はこれだけでOK。（拡張もしやすい）
    language: str = "ja"        # "ja" | "en" など
    audience: Optional[str] = None  # 誰宛か（任意）

class GreetResponse(BaseModel):
    model: str
    text: str


async def call_gemini(model: str, prompt: str, timeout: float = 20.0) -> str:
    """
    Gemini への呼び出し（APIキーが無い or MOCK_MODE の場合はモック応答）。

    - 実API: REST/POST v1beta models/{model}:generateContent
    - レスポンスの text を抽出して返却
    """
    if MOCK_MODE or not GOOGLE_API_KEY:
        # サンプルとして少し遅延してモック応答
        await asyncio.sleep(1 if "lite" in model else 3)
        return f"[MOCK:{model}] {prompt} に対するサンプル応答です。こんにちは！"

    url = f"{GEMINI_API_BASE}/models/{model}:generateContent?key={GOOGLE_API_KEY}"

    payload: Dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ]
    }

    # httpx の AsyncClient でタイムアウト＆リトライ簡易実装
    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()

            # v1beta 応答の標準的取り出し（候補1の最初の part）
            candidates = data.get("candidates", [])
            if not candidates:
                raise ValueError("No candidates in Gemini response")

            parts = candidates[0].get("content", {}).get("parts", [])
            for p in parts:
                if "text" in p:
                    return p["text"]

            # 互換用のフォールバック
            if "text" in candidates[0].get("content", {}):
                return candidates[0]["content"]["text"]

            raise ValueError("No text part in Gemini response")
        except Exception as e:
            if attempt == 1:
                raise HTTPException(status_code=502, detail=f"Gemini call failed: {e}")

    # 到達しないはず
    return ""


# ====== エンドポイント ======

@app.post("/api/gemini/flash-lite/greet", response_model=GreetResponse)
async def greet_flash_lite(req: GreetRequest):
    """1) gemini-2.5-flash-lite に「あいさつを返す」"""
    prompt = "短く丁寧に挨拶を返してください。" if req.language.startswith("ja") else "Please reply with a short, polite greeting."
    if req.audience:
        prompt += f" 相手は「{req.audience}」です。"
    text = await call_gemini(MODEL_FLASH_LITE, prompt)
    return GreetResponse(model=MODEL_FLASH_LITE, text=text)


@app.post("/api/gemini/flash/greet", response_model=GreetResponse)
async def greet_flash(req: GreetRequest):
    """2) gemini-2.5-flash に「あいさつを返す」"""
    prompt = "短く丁寧に挨拶を返してください。" if req.language.startswith("ja") else "Please reply with a short, polite greeting."
    if req.audience:
        prompt += f" 相手は「{req.audience}」です。"
    text = await call_gemini(MODEL_FLASH, prompt)
    return GreetResponse(model=MODEL_FLASH, text=text)


@app.post("/api/gemini/flash/greet_best", response_model=GreetResponse)
async def greet_flash_best(req: GreetRequest):
    """3) gemini-2.5-flash に「最高の挨拶を考えて返す」"""
    prompt = (
        "最高の挨拶を1文で考えて返してください。"
        if req.language.startswith("ja")
        else "Craft the best possible greeting in one sentence and return it."
    )
    if req.audience:
        prompt += f" 相手は「{req.audience}」です。"
    text = await call_gemini(MODEL_FLASH, prompt)
    return GreetResponse(model=MODEL_FLASH, text=text)


# おまけ: ヘルスチェック
@app.get("/api/health", include_in_schema=False)
async def health():
    return {"ok": True, "mock": MOCK_MODE}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)