import time
import json
import html
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# ===== Template =====
PAGE_TEMPLATE_PATH = Path("html_render_templates/summary_first.html")

SECTION_BLOCK_TEMPLATE = """<section class="report-section">
  <h2 class="section-title">{title}</h2>
  <p class="section-abstruct">{abstruct}</p>
  {keyframe_block}
</section>
"""

KEYFRAME_BLOCK_TEMPLATE = """<div class="image-placeholder">
  <!-- スクリーンショットの挿入場所 -->
  <screenshot time="{time}" />
</div>
"""

def pick_first_scene_keyframe_time(sec: Dict[str, Any]) -> Optional[str]:
    """
    要約1枚を出すためにシーンの中の最初のキーフレームのタイムスタンプ
    sections.scenes[0].keyframe.timestamp を抽出。
    - scenes or keyframe が無い/空なら None
    """
    scenes = sec.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        return None

    first = scenes[0]
    kf = first.get("keyframe")
    if isinstance(kf, dict):
        ts = kf.get("timestamp")
        return ts if ts is not None else None
    return None

def render_sections_for_first_summary(sections: List[Dict[str, Any]]) -> str:
    """
    セクションを要約の最初のテンプレートに流し込むためのヘルパー関数
    """
    blocks: List[str] = []
    for sec in sections or []:
        title = html.escape(str(sec.get("title", "")))
        abstruct = html.escape(str(sec.get("abstruct", "")))
        ts = pick_first_scene_keyframe_time(sec)

        if ts:
            keyframe_block = KEYFRAME_BLOCK_TEMPLATE.format(time=html.escape(ts))
        else:
            keyframe_block = ""  # 画像プレースホルダーは出さない

        block = SECTION_BLOCK_TEMPLATE.format(
            title=title,
            abstruct=abstruct,
            keyframe_block=keyframe_block
        )
        blocks.append(block)
    return "\n".join(blocks)

def render_page_for_first_summary(page_template: str, data: Dict[str, Any]) -> str:
    """
    GemniのレスポンスJSONを要約の最初のテンプレートに流し込む関数
    """
    title = html.escape(str(data.get("title", "")))
    abstruct = html.escape(str(data.get("abstruct", "")))
    sections_html = render_sections_for_first_summary(data.get("sections", []))

    html_out = (
        page_template
        .replace("{{title}}", title)
        .replace("{{abstruct}}", abstruct)
        .replace("{{sections}}", sections_html)
    )
    return html_out

def json_to_markdown(data: dict) -> str:
    """
    要約したJSONを以下のマークダウン形式に変換する
    ```
    # タイトル
    概要 
    ## セクション 
    セクション概要 
    ### シーン1 
    シーン1概要 
    ```
    """
    lines = []

    # Title
    title = (data.get("title") or "").strip()
    if title:
        lines.append(f"# {title}")

    # 概要
    overview = data.get("abstruct" or "").strip()
    if overview:
        lines.append(overview)

    # セクション
    for section in data.get("sections", []):
        sec_title = (section.get("title") or "").strip()
        if sec_title:
            lines.append(f"## {sec_title}")

        sec_overview = (section.get("abstruct") or "").strip()
        if sec_overview:
            lines.append(sec_overview)

        # シーン
        for idx, scene in enumerate(section.get("scenes", []), start=1):
            lines.append(f"### シーン{idx}")
            desc = (scene.get("description") or "").strip()
            if desc:
                lines.append(desc)

    return "\n\n".join(lines).rstrip()

# ref: https://ai.google.dev/gemini-api/docs/google-search?hl=ja#python_1 を参考に作成
# Gemini with Googleサーチからのレスポンスを整形して引用付きで返す関数
def add_citations(response):
    text = response.text
    supports = response.candidates[0].grounding_metadata.grounding_supports
    chunks = response.candidates[0].grounding_metadata.grounding_chunks

    # # Sort supports by end_index in descending order to avoid shifting issues when inserting.
    # sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    for support in supports:
        text_ = support.segment.text
        # end_index = support.segment.end_index 
        # end_index はズレている？のでテキストで一致する場所を判定
        if support.grounding_chunk_indices:
            # Create citation string like [1](link1)[2](link2)
            citation_links = []
            for i in support.grounding_chunk_indices:
                if i < len(chunks):
                    # url とタイトル/domainを取得
                    uri = chunks[i].web.uri
                    title = chunks[i].web.title
                    domain = chunks[i].web.domain
                    # 上記 uri はリダイレクトの URL が取得される。requests で正規の URL を取得することもできるが処理時間の関係で実行せず
                    # url, title = fetch_url_and_title(uri)
                    # if url == "Fail": # url fetch で何らかのエラーが生じている
                    #     continue
                    citation_links.append(f"[{i + 1}] (title: {title})")

            citation_string = ", ".join(citation_links)
            end_index = text.find(text_) + len(text_) - 1 # 一致するテキストのインデックスを取得（最初に一致したインデックスのみ）
            text = text[:end_index] + citation_string + text[end_index:]

    return text

def fetch_url_and_title(url: str) -> tuple[str, str]:
    """
    GeminiのWeb検索で拾ってきたリダイレクトURLから正規のURLとタイトルを取得
    リクエストに失敗した場合は、適当な文字列を返す
    """
    # リトライを無効化したセッション
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=0))
    session.mount("http://", HTTPAdapter(max_retries=0))

    try:
        response = session.get(url, timeout=1)  # タイムアウト明示
        parsed_url = urlparse(response.url)
        domain = parsed_url.netloc or "unknown.domain"

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else domain

        return response.url, title

    except RequestException as e:
        # SSLエラーも含めて requests のエラーは全部ここで握る
        print(f"[ERROR] {e}")
        fallback_url = "Fail"
        fallback_title = "Fail"
        return fallback_url, fallback_title


def build_keywords_list(data):
    """
    KEYWORDS_SCHEMA に従った JSON から
    { "keyword": ..., "explanation": "説明文（出典: ...）" } のリストを生成する
    """
    result = []

    for entry in data.get("keywords", []):
        keyword = entry["keyword"]
        explanation = entry["explanation"]
        citations = entry.get("citations", [])

        if not citations:
            # cite_text = "出典: 不明"
            # 出典がなければスキップ（ハルシネーションの疑いがあるためフロントに返さない）
            continue
        else:
            # 引用先のタイトルリストを取得
            titles = [c["title"] for c in citations]
            # # 16文字以降を「…」に省略
            # if len(title) > 15:
            #     title = title[:15] + "…"

            if len(citations) > 3:
                cite_text = f"出典: {", ".join(titles[:3])} など" # 3件まで載せる
            else:
                cite_text = f"出典: {", ".join(titles)}"

        result.append({
            "keyword": keyword,
            "explanation": f"{explanation}（{cite_text}）"
        })

    return result


def annotate_scene(scene, keywords_array, already_assigned):
    """
    引用付きの要約JSONを作成するためのヘルパー
    
    scene の記述内容内に抽出したキーワードがあればappendixフィールドをいれる
    複数シーンで同じキーワードがあった場合は最初のシーンのみにAppendixを入れる
    Appendixがあるシーンにはキーワードに*をつける（複数ある場合は*の数を増やす）
    """
    desc = scene.get("description", "")
    if not desc:
        return set()

    # --- 最長一致・非重複のマッチ列を構築（長いキーワード優先） ---
    kws_sorted = sorted(keywords_array, key=lambda k: len(k["keyword"]), reverse=True)
    matches = []  # (start, end, kw_obj)
    i = 0
    while i < len(desc):
        hit = None
        for kw_obj in kws_sorted:
            kw = kw_obj["keyword"]
            if desc.startswith(kw, i):
                hit = kw_obj
                break
        if hit:
            start, end = i, i + len(hit["keyword"])
            matches.append((start, end, hit))
            i = end
        else:
            i += 1

    if not matches:
        return set()

    # --- appendix 対象キーワードを決定（全体で初登場のみ） ---
    appendix = []
    star_map = {}
    next_star = 1
    appended_now = set()
    for _, _, kw_obj in matches:
        kw = kw_obj["keyword"]
        if kw not in already_assigned:
            if kw not in star_map:  # 初登場のものだけ * を割り当て
                star_map[kw] = next_star
                next_star += 1
            if kw not in appended_now:  # appendix も初登場にだけ
                appendix.append({
                    "keyword": kw,
                    "explanation": kw_obj["explanation"]
                })
                appended_now.add(kw)
                already_assigned.add(kw)

    # --- description を再構築（初登場のものだけ * を付与） ---
    if star_map:
        parts = []
        last = 0
        for start, end, kw_obj in matches:
            kw = kw_obj["keyword"]
            if kw in star_map:
                parts.append(desc[last:start])
                parts.append(desc[start:end] + ("*" * star_map[kw]))
                last = end
            else:
                # 既出キーワードはそのまま
                parts.append(desc[last:end])
                last = end
        parts.append(desc[last:])
        scene["description"] = "".join(parts)

    # --- appendix を追加 ---
    if appendix:
        scene["appendix"] = appendix

    return appended_now

