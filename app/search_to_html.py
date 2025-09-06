import json
import re
import domain.gemini as gem
import domain.postprocessing as ps

# sample_output.jsonを開いてsample_jsonに格納
# with open('sample_output.json', 'r') as f:
#     sample_json = json.load(f)

# # 要約結果を検索をかけるためにマークダウン形式に変更
# markdown_text = ps.json_to_markdown(sample_json)
# print(markdown_text)

# # 補足情報と検索結果を取得
# text, res = gem.search_supp_info(markdown_text)
# print(res)

# # 引用を付与
# text_with_supp = ps.add_citations(res)
# print(text_with_supp)

# # キーワードリストを取得
# supp_json, _ = gem.format_supp_to_json(text_with_supp)

# # for debug
# with open("keyword.json", "w", encoding="utf-8") as f:
#     json.dump(supp_json, f, ensure_ascii=False, indent=2)

# with open('keyword.json', 'r') as f:
#     keyword_json = json.load(f)

# keywords_list = ps.build_keywords_list(keyword_json)

# # 全シーンへ適用
# assigned_keywords = set()

# for section in sample_json["sections"]:
#     for s in section["scenes"]:
#         ps.annotate_scene(s, keywords_list, assigned_keywords)

# print(json.dumps(sample_json, ensure_ascii=False, indent=2))

# # for debug
# with open("sample_output_appendix.json", "w", encoding="utf-8") as f:
#     json.dump(sample_json, f, ensure_ascii=False, indent=2)

with open('sample_output_appendix.json', 'r') as f:
    sample_appendix_json = json.load(f)

