import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt.prompt import VIDEO_SUMMARY_PROMPT
from prompt.json_schema import SUMMARY_SCHEMA

# =================================
# Gemini 推論設定
# =================================
load_dotenv() # GOOGLE_APPLICATION_CREDENTIALS を読み込む
# GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
LOCATION = os.environ["LOCATION"]
BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]

# Geminiクライアント初期化
# client = genai.Client(api_key=GEMINI_API_KEY)
__client = genai.Client(
    vertexai=True,
    project=GCP_PROJECT_ID,
    location=LOCATION,
    http_options=types.HttpOptions(api_version="v1")
  )

async def video_summary_with_caption_v2():
    blob_name = "kaji.mp4"
    lang = "ja"
    video_length_sec = 205
    hms = "0:03:25"
    print("動画の長さ: " + hms)

    prompt = VIDEO_SUMMARY_PROMPT.format(
        lang=lang,
        hms=hms
    )

    response_schema = SUMMARY_SCHEMA

    __using_model = "gemini-2.5-flash"
    __thinking_budget = -1
    print(f"thinking budget: {__thinking_budget}")

    # 動画のinput
    gs_url = f"gs://{BUCKET_NAME}/{blob_name}"
    _, ext = os.path.splitext(blob_name)
    ext = ext.lower()

    input_video = types.Part(
        file_data = types.FileData(file_uri=gs_url, mime_type = f"video/{ext}"),
        # video_metadata = types.VideoMetadata(
        #             start_offset='0s',
        #             end_offset='1s'
        # )
    )
    # promptのinput
    input_prompt = types.Part.from_text(text=prompt.strip())

    contents = [
        types.Content(
            role = "user",
            parts = [
                input_video,
                input_prompt
            ]
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature = 0,
        top_p = 1,
        seed = 0,
        max_output_tokens = 65535,
        thinking_config=types.ThinkingConfig(thinking_budget=__thinking_budget),
        mediaResolution="MEDIA_RESOLUTION_LOW",
        response_modalities = ["TEXT"],
        safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
                )
            ],
        response_mime_type = "application/json",
        response_schema = response_schema,
    )

    response = await __client.aio.models.generate_content(
        model = __using_model,
        contents = contents,
        config = generate_content_config
    )

    # print(response.parsed)

    return response.parsed

