# import domain.gemini as gem
# import asyncio
# import json

# async def main():
#     res_json = await gem.video_summary_with_caption_v2()
#     print(json.dumps(res_json, indent=2, ensure_ascii=False))

# asyncio.run(main())


import json
from pathlib import Path
import domain.postprocessing as ps

# 読み込みたい JSON ファイルのパス
json_path = Path("output/sample.json")

# ファイルを読み込み、Python の dict に変換
with json_path.open(encoding="utf-8") as f:
    data = json.load(f)

# 読み込んだ内容を確認
print(type(data))   # dict
print(data["title"])  # タイトルを確認

# テンプレート読込
template_str = ps.PAGE_TEMPLATE_PATH.read_text(encoding="utf-8")
# HTML 生成
html_out = ps.render_page_for_first_summary(template_str, data)

# 出力（標準出力）
print(html_out)
