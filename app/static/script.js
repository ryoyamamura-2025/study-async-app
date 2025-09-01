// static/script.js

/**
 * ==== クライアントが知る必要があるのは “エンドポイント” と “リクエスト型/レスポンス型” だけ ==== 
 *
 * Request (JSON):
 *   {
 *     language: "ja" | "en",  // default "ja"
 *     audience?: string       // 任意
 *   }
 *
 * Response (JSON):
 *   {
 *     model: string,
 *     text: string
 *   }
 */

const API_BASE = "/api";

const $ = (sel) => document.querySelector(sel);
const startBtn = $("#startBtn");
const spinner = $("#spinner");
const chatBox = $("#chatBox");

function setBusy(busy) {
  spinner.hidden = !busy;
  spinner.setAttribute("aria-busy", busy ? "true" : "false");
  startBtn.disabled = busy;
}

async function postJSON(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body ?? {}),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
  return /** @type {{model:string, text:string}} */ (await res.json());
}

function appendLine(line) {
  chatBox.value += (chatBox.value ? "\n" : "") + line;
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function startChat() {
  setBusy(true);
  chatBox.value = ""; // クリア

  // クライアントから渡すデータ型はこれだけ（サンプル）
  const payload = { language: "ja" /*, audience: "お客様" */ };

  // 1) lite（戻り次第すぐ表示）
  const p1 = postJSON("/gemini/flash-lite/greet", payload)
    .then((r) => {
      appendLine(`【1:${r.model}】\n${r.text}`);
      return r;
    });

  // 2) flash
  const p2 = postJSON("/gemini/flash/greet", payload);

  // 3) flash（最高の挨拶）
  const p3 = postJSON("/gemini/flash/greet_best", payload);

  try {
    // 1 は待たずに先に出す（p1.then でやっている）
    // 2 と 3 は両方揃ってから追記
    const [, r2, r3] = await Promise.all([p1, p2, p3]);
    appendLine("\n— ②③ の結果 —");
    appendLine(`【2:${r2.model}】\n${r2.text}`);
    appendLine(`【3:${r3.model}】\n${r3.text}`);
  } catch (err) {
    console.error(err);
    appendLine(`⚠ エラーが発生しました: ${err instanceof Error ? err.message : String(err)}`);
  } finally {
    setBusy(false);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  startBtn.addEventListener("click", startChat);
});
