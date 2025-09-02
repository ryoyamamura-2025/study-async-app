# Study Async App
バックエンドで非同期処理を実行するWebアプリ開発の勉強  
環境構築を Docker + UV で行い、Cloud run にデプロイする

## 環境構築
1. UV で仮想環境構築
```
mkdir study-async-app
cd study-async-app
uv init 
uv venv
uv add fastapi uvicorn
```

2. `app` ディレクトリに `main.py` で FastAPI のアプリを作成しスクリプトで起動
```
bash rebuild.sh
```

3. uvicorn のホットリロードで実行しているので、スクリプト編集が即座に反映される

## Cloud run へのデプロイ
デプロイ用のスクリプトを実行（プロジェクト ID 等は適切に設定）
```
cp deploy.sh.dev deploy.sh
bash deploy.sh
```

## トラブルシューティング
- ローカル開発用コンテナの起動スクリプト：Dockerfile で app ディレクトリ配下のみイメージにコピーしているが、 `docker run ~~ -v "$PWD":/app ~~` としてしまうと、マウントしたディレクトリで上書きされてしまうので注意。ローカル開発時は `-v "$PWD":/workspace -w /workspace/app` で解決。

## 参考
- uv on docker: [uv 公式ドキュメント](https://docs.astral.sh/uv/guides/integration/docker/#non-editable-installs)