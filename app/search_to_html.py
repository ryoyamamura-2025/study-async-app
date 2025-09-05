import json
import re
import domain.gemini as gem
import domain.postprocessing as ps

# sample_output.jsonを開いてsample_jsonに格納
with open('sample_output.json', 'r') as f:
    sample_json = json.load(f)

markdown_text = ps.json_to_markdown(sample_json)
print(markdown_text)

text, res = gem.search_supp_info(markdown_text)
print(res)

text_with_supp = ps.add_citations(res)
print(text_with_supp)