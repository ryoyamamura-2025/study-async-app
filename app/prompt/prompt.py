# Required: lang, hms
VIDEO_SUMMARY_PROMPT = \
"""
あなたは動画要約のプロです。以下のタスクに取組んでください。

<task>
与えられた動画の内容を正確に要約し、指定されたスキーマのJSONを生成してください。
output_language = {lang}
video_total_length = {hms}
</task>

<condition>
- 動画の長さが2分以下の場合は、セクション数は3個以下、セクション内のシーンの数は1つにすること
- 説明文は常に第三者の視点で動画から読み取ることのできる客観的な事実のみを記載すること
- 文章は「です」「ます」調にすること
</condition>
"""

# Required: lang, input_text
SUPP_INFO_PROMPT =\
"""
あなたは検索と関連情報付与の専門家です。以下のタスクに取り組んでください。

<task>
input_textタグで与えられた文章の内容を補足し、読み手の理解を向上させるための有益な補足情報を提供してください。
キーワードを抽出し、その後、Web検索を使用してキーワードに関するを取得してください。
output_language = {lang}
</task>

<condition>
- キーワードは文章の中の主要な事実や出来事、専門用語、固有名詞（組織名、人名、地名）をピックアップすること。
- 推測は避け必ずWeb検索を用いて最新かつ正確な情報を提供すること。
</condition>

<output structure>
- キーワード1
[キーワードに関する補足情報]
- キーワード2
[キーワードに関する補足情報]
</output structure>

<input_text>
{input_text}
</input_text>
"""