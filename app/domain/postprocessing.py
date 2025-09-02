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
