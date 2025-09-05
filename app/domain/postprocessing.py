import json
import html
from pathlib import Path
from typing import Any, Dict, List, Optional

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

# ref: https://ai.google.dev/gemini-api/docs/google-search?hl=ja#python_1
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
        if support.grounding_chunk_indices:
            # Create citation string like [1](link1)[2](link2)
            citation_links = []
            for i in support.grounding_chunk_indices:
                if i < len(chunks):
                    uri = chunks[i].web.uri
                    citation_links.append(f"[{i + 1}]({uri})")

            citation_string = ", ".join(citation_links)
            end_index = text.find(text_) + len(text_) - 1
            text = text[:end_index] + citation_string + text[end_index:]

    return text