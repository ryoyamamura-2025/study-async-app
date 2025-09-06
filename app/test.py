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

import domain.postprocessing as ps
url, title = ps.fetch_final_url_and_title("https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFOcvoIb7txqqb8eyQkB_oXqJs0TVU-yeG2LwMIQENAxyVd4cbYfXihdeeX8yfJyK-RYjU0bph6A_PrFMjL_JtlLmppduP1NwlfO0LNG_dnfySOjktQpMYDHaYafY6A-ImMDM09gCM=")
print(url)
print(title)
