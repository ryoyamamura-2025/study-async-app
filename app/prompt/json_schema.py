# SUMMARY_SCHEMA
"""
{
    "title": 動画のタイトル str 必須,
    "abstruct": 動画全体の短い要約 str 必須,
    "sections": [
        "title": セクションのタイトル str 必須,
        "abstruct": セクション全体の短い要約 str 必須,
        "scenes": [
            {
                "description": シーンの内容を説明する本文 str, 必須
                "keyframe": {
                    "timestamp": タイムスタンプ(H:MM:SS形式) str,
                    "description": フレームの簡易な説明文
                } 動画を理解する上で重要な場面（動画内の重要なトピックを説明している図やスライド）のスクリーンショット 必須ではない
            },
            ...
        ] サブセクションの数は1~4個まで
    ] セクションの数は3~7個まで
}
"""

SUMMARY_SCHEMA = {
  "type": "object",
  "description": "動画全体の構造化された要約",
  "properties": {
    "title": { "type": "string", "description": "動画のタイトル" },
    "abstruct": { "type": "string", "description": "動画全体の要約" },
    "sections": {
      "type": "array",
      "description": "動画の主要セクション一覧（3〜7個）",
      "minItems": 3,
      "maxItems": 7,
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string", "description": "セクションのタイトル" },
          "abstruct": { "type": "string", "description": "セクション全体の短い要約" },
          "scenes": {
            "type": "array",
            "description": "シーンの一覧（1〜4個）",
            "minItems": 1,
            "maxItems": 4,
            "items": {
              "type": "object",
              "properties": {
                "description": { "type": "string", "description": "シーンの内容を説明する本文 (200~300文字・3~5文程度)" },
                "keyframe": {
                  "type": "object",
                  "description": "動画理解に重要なフレーム（任意）",
                  "properties": {
                    "timestamp": { "type": "string", "description": "H:MM:SS 形式のタイムスタンプ" },
                    "description": { "type": "string", "description": "フレームの簡易な説明文" }
                  },
                  "required": ["timestamp", "description"]
                }
              },
              "required": ["description"]
            }
          }
        },
        "required": ["title", "abstruct", "scenes"]
      }
    }
  },
  "required": ["title", "abstruct", "sections"]
}

KEYWORDS_SCHEMA = {
  "type": "object",
  "description": "キーワードの辞書（キーワードと説明、出典リンクの一覧）",
  "properties": {
    "keywords": {
      "type": "array",
      "description": "キーワードエントリ一覧",
      "items": {
        "type": "object",
        "properties": {
          "keyword": {
            "type": "string",
            "description": "キーワード",
          },
          "explanation": {
            "type": "string",
            "description": "キーワードの説明文",
          },
          "citations": {
            "type": "array",
            "description": "出典/参考リンクの配列",
            "items": {
              "type": "object",
              "properties": {
                "title": {
                  "type": "string",
                  "description": "出典のタイトル",
                },
                "url": {
                  "type": "string",
                  "description": "出典URL",
                }
              },
              "required": ["title", "url"],
            }
          }
        },
        "required": ["keyword", "explanation", "citations"],
      }
    }
  },
  "required": ["keywords"],
}