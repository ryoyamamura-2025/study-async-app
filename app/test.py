# import domain.gemini as gem
# import asyncio
# import json

# async def main():
#     res_json = await gem.video_summary_with_caption_v2()
#     print(json.dumps(res_json, indent=2, ensure_ascii=False))

# asyncio.run(main())

# import domain.gemini as gem
# import json
# import asyncio

# async def main():
#     res_json, _ = await gem.video_summary_with_caption_v2()
#     print(json.dumps(res_json, indent=2, ensure_ascii=False))

# asyncio.run(main())

# import json
# from pathlib import Path
# import domain.postprocessing as ps

# # 読み込みたい JSON ファイルのパス
# json_path = Path("output/sample.json")

# # ファイルを読み込み、Python の dict に変換
# with json_path.open(encoding="utf-8") as f:
#     data = json.load(f)

# # 読み込んだ内容を確認
# print(type(data))   # dict
# print(data["title"])  # タイトルを確認

# # テンプレート読込
# template_str = ps.PAGE_TEMPLATE_PATH.read_text(encoding="utf-8")
# # HTML 生成
# html_out = ps.render_page_for_first_summary(template_str, data)

# # 出力（標準出力）
# print(html_out)


text = """
旋盤の基本的な操作方法に関する動画の内容を補足し、読み手の理解を深めるための情報を提供します。

-   **旋盤**
    旋盤（Lathe）は、工作機械の一種で、主軸に取り付けた加工物（ワーク）を回転させ、バイトと呼ばれる切削工具を当てて削り取ることで加工を行う機械です。主に円筒形や円盤状の加工物の外丸削り、面削り、テーパ削り、中ぐり、穴あけ、突切り、ねじ切りなどの加工が可能です。
    旋盤には、手動で操作する汎用旋盤（普通旋盤）や、プログラムされた指示に従って自動で作業を行うNC旋盤（数値制御旋盤）など、様々な種類があります。 フライス加工が工具を回転させて加工するのに対し、旋盤加工は加工物を回転させる点が異なります。

-   **ミクロンチャンネル**
    ミクロンチャンネルは、YouTubeで旋盤の操作方法などを解説しているチャンネルです。動画の解説者であるユウと、相方のカズが登場します。彼らは自身を整備士であり、専門の旋盤工ではないと前置きしつつ、動画で頻繁に使用する小型旋盤の操作について紹介しています。

-   **回転数**
    旋盤における回転数とは、主軸が1分間に回転する回数を指します。 この回転数は、切削速度の調整に直結し、加工精度、工具の寿命、作業効率、製品の品質に大きな影響を与える重要な要素です。 回転数が高ければ切削速度も速くなり、加工時間を短縮できますが、工具の摩耗も早まるため、加工物の材質や加工内容に応じて最適な回転数を設定する必要があります。

-   **送り方向**
    送り方向とは、切削工具が加工物に対して移動する方向を指します。旋盤では、加工物の軸に沿って移動する「縦送り（長手方向）」や、軸に垂直に移動する「横送り（端面方向）」があります。 これらの送り方向は、レバー操作によって手動または自動で調整されます。

-   **送り速度**
    送り速度とは、旋盤の主軸が1回転する間に切削工具が移動する距離（mm/rev）を指します。 送り速度は、加工物の表面粗さ、加工時間、切りくずの出方に影響を与えます。 送り速度を大きくすると加工時間は短縮されますが、加工面の表面は粗くなる傾向があります。

-   **切削加工**
    切削加工とは、切削工具を用いて金属などの加工物を削ったり、切断したりして、目的の形状に作り出す加工技術の総称です。 旋盤加工やフライス加工などが切削加工に含まれ、機械加工の代表的な方法の一つです。 切削加工は、「切削（材料を削り取る動き）」と「送り（工具や加工対象を移動させる動き）」の二つの動作を組み合わせて行われます。

-   **ネジ切り**
    ネジ切り（ねじ切り加工）は、旋盤を用いて加工物にねじ山を形成する加工方法です。 正確なねじ山を切削するためには、主軸の回転と送りの動きを厳密に同期させる必要があります。 専用のねじ切り工具が使用されます。

-   **荒削り**
    荒削り（荒加工）とは、機械加工において、最終的な仕上げ加工を行う前の段階で実施される粗い加工工程です。 主な目的は、素材から大量の材料を効率的に除去し、製品のおおよその形状を作り出すことです。 この工程では、深い切り込みと速い送り速度が特徴で、表面は粗くなります。

-   **仕上げ加工**
    仕上げ加工とは、設計図面や製品仕様で決められた寸法精度や表面品質に合わせるための最終的な加工方法です。 荒削りとは異なり、より小さな切り込みと遅い送り速度で行われ、滑らかな表面と高い精度を実現します。 研磨加工や研削加工、超仕上げ加工、鏡面加工なども仕上げ加工の一種です。

-   **チャック**
    チャックとは、旋盤などの工作機械の主軸に取り付けられ、加工物を固定・保持するための機器です。 加工物を正確かつ強固に把握し、主軸の回転を加工物に伝達する役割を担います。
    主な種類には、3つの爪が同時に動いて求心作用がある「スクロールチャック（連動チャック）」や、4つの爪が独立して動き、非対称な加工物や精密な芯出しに適した「インディペンデントチャック（単動チャック）」などがあります。

-   **自動送り**
    自動送りとは、汎用旋盤において、一定の送り速度を維持して加工を行うための機能です。 主軸の回転と同期して、切削工具を自動で移動させることができます。 これにより、手動操作では難しい安定した加工が可能となり、ねじ切り加工などにも用いられます。 縦送り（長手方向）と横送り（端面方向）の自動送りが可能です。
""".strip()

print(text[337:545])

# import domain.postprocessing as ps
# url, title = ps.fetch_url_and_title("ああああ")
# print(url)
# print(title)
import json

# サンプルJSON
data = {
    "scenes": [
        { "id": 1, "description": "朝の街並み。通勤する人々が忙しそうに歩いている。" },
        { "id": 2, "description": "公園で子供たちが遊んでいる。太陽が木漏れ日を作っている。" },
        { "id": 3, "description": "公園の近くの海辺では、街から来た人々が散歩している。" },
        { "id": 4, "description": "街は夜になると賑わい、海辺では潮風が強くなる。" }
    ]
}

# キーワード配列
keywords = [
    { "keyword": "街", "explanation": "建物や道路が集まり、人々が生活している地域" },
    { "keyword": "海", "explanation": "広大な水域で、多くの生命を育む場所" },
    { "keyword": "公園", "explanation": "市民の憩いの場として利用される緑地" },
    { "keyword": "海辺", "explanation": "海に面した沿岸部" },
]

def annotate_scene(scene, keywords_array, already_assigned):
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

# 全シーンへ適用
assigned_keywords = set()
for s in data["scenes"]:
    annotate_scene(s, keywords, assigned_keywords)

print(json.dumps(data, ensure_ascii=False, indent=2))


import json

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
            title = citations[0]["title"]
            # 16文字以降を「…」に省略
            if len(title) > 15:
                title = title[:15] + "…"

            if len(citations) > 1:
                cite_text = f"出典: {title} など"
            else:
                cite_text = f"出典: {title}"

        result.append({
            "keyword": keyword,
            "explanation": f"{explanation}（{cite_text}）"
        })

    return result

# --- 動作テスト用 ---
sample_json = {
    "keywords": [
        {
            "keyword": "街",
            "explanation": "建物や道路が集まり、人々が生活している地域",
            "citations": [
                {"title": "とても長い長い参考文献タイトルABCDEF", "url": "https://example.com"},
                {"title": "別の出典", "url": "https://example.org"}
            ]
        },
        {
            "keyword": "海",
            "explanation": "広大な水域で、多くの生命を育む場所",
            "citations": [
                {"title": "海洋学の基礎", "url": "https://example.com"}
            ]
        }
    ]
}

print(json.dumps(build_keywords_list(sample_json), ensure_ascii=False, indent=2))
